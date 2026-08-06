# Hardened Multi-Stage Patterns

Digests below are placeholders (`sha256:...`) — replace with the real digest of the tag you pull (`docker buildx imagetools inspect <image>:<tag>`). Never ship the placeholder.

## Go (static binary → scratch/distroless)

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22.5-bookworm@sha256:... AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /app ./cmd/server

FROM gcr.io/distroless/static-debian12:nonroot@sha256:...
WORKDIR /
COPY --from=build /app /app
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app"]
```

## Node.js (build deps dropped in final)

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20.14.0-slim@sha256:... AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --omit=dev

FROM node:20.14.0-slim@sha256:...
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/dist ./dist
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD node -e "require('http').get('http://127.0.0.1:3000/health',r=>process.exit(r.statusCode===200?0:1)).on('error',()=>process.exit(1))"
ENTRYPOINT ["node", "dist/server.js"]
```

## Python (virtualenv copied to slim runtime)

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12.4-slim-bookworm@sha256:... AS build
WORKDIR /app
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12.4-slim-bookworm@sha256:...
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin appuser
WORKDIR /app
COPY --from=build /venv /venv
COPY --chown=appuser:appuser . .
ENV PATH="/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER 10001
EXPOSE 8000
ENTRYPOINT ["python", "-m", "app"]
```

## Java (JRE-only runtime, jlink/distroless)

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21.0.3_9-jdk-jammy@sha256:... AS build
WORKDIR /src
COPY . .
RUN ./mvnw -q -DskipTests package

FROM gcr.io/distroless/java21-debian12:nonroot@sha256:...
WORKDIR /app
COPY --from=build /src/target/app.jar /app/app.jar
USER nonroot
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

## Build-time secret (BuildKit — never bakes into a layer)

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
```
Build with: `docker build --secret id=npmrc,src=$HOME/.npmrc .`

## `.dockerignore` (starter)

```
.git
.gitignore
**/node_modules
**/.env*
**/*.pem
**/*.key
**/secrets*
dist
build
coverage
Dockerfile*
*.md
```

## Recommended runtime flags (docker run / compose)

```
docker run \
  --read-only --tmpfs /tmp \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --user 10001:10001 \
  --memory=512m --cpus=1 \
  myimage@sha256:...
```

Compose equivalent: `read_only: true`, `cap_drop: [ALL]`, `security_opt: ["no-new-privileges:true"]`, `user: "10001"`, `mem_limit`, plus a `tmpfs` for writable paths.
