# A PLACEHOLDER that runs. Replace it with a real build for your System Under
# Test — but read why it is shaped this way first.
#
# What it must do, whatever you put here:
#   1. Run with no manual steps. Week 3 puts it under load and Week 4 deploys
#      it; neither can stop to ask you a question.
#   2. Expose a health endpoint the smoke stage can call.
#   3. Actually start. Week 0's last exit gate is `docker compose up -d --wait`,
#      which blocks until the HEALTHCHECK below passes.
#
# THIS FILE USED TO BE A MAVEN BUILD, and it could not satisfy (3) for anybody.
# It ran `mvn package` over a tree with no src/main/java, produced a jar with no
# Main-Class, and `java -jar` exited with "no main manifest attribute" — so the
# container never became healthy, `--wait` blocked until timeout, and Week 0's
# final step failed. It was also hard-coded to Java in a repository whose entire
# design is that the pipeline never names a language: a Python, C++ or .NET
# learner's LoadTest, Security and A11y stages all tried to build a Maven image.
#
# So what ships is a placeholder with no build step and no language opinion.
# It exists to prove the pipeline works end to end before you have an
# application. The multi-stage Java version is kept at the bottom as a worked
# example, because multi-stage IS the right shape once you have something to
# build: the runtime image should not carry your build tools, and a smaller
# image is a smaller attack surface for the Week 3 scan.

FROM python:3.12-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --chown=app:app placeholder-app.py .
USER app
EXPOSE 8080

HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=5 \
  CMD wget -qO- http://127.0.0.1:8080/health || exit 1

ENTRYPOINT ["python3", "placeholder-app.py"]

# ---------------------------------------------------------------------------
# Worked example — a real multi-stage Java build. Delete everything above and
# uncomment this once you have sources at src/main/java and a <mainClass> (or
# the Spring Boot plugin) in profiles/java/pom.xml. Note maven:, not
# eclipse-temurin: — the JDK image carries no `mvn`.
#
# FROM maven:3.9-eclipse-temurin-17 AS build
# WORKDIR /build
# COPY profiles/java/pom.xml .
# RUN --mount=type=cache,target=/root/.m2 mvn -B -ntp dependency:go-offline
# COPY src ./src
# RUN --mount=type=cache,target=/root/.m2 mvn -B -ntp package -DskipTests
#
# FROM eclipse-temurin:17-jre-alpine
# RUN addgroup -S app && adduser -S app -G app
# WORKDIR /app
# COPY --from=build /build/target/*.jar app.jar
# USER app
# EXPOSE 8080
# HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=5 \
#   CMD wget -qO- http://127.0.0.1:8080/health || exit 1
# ENTRYPOINT ["java", "-jar", "/app/app.jar"]
