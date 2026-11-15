# Genos application skeleton

Platform-owned iOS and Android project structure. This contains no product business logic or passing placeholder tests.

The installer assigns a development application identifier to both platforms and generates the Xcode project with XcodeGen. Configure store-owned identifiers and signing credentials before publishing. No signing team, keystore, payment account or production endpoint is included.

The Gradle wrapper comes from the Gradle 9.7.1 release; its JAR SHA-256 is `7a9ce74cff467ca1bf60a4fcd9f05185acceda4d0f382434d393e17864262c5d`. The distribution checksum is pinned in `android/gradle/wrapper/gradle-wrapper.properties`.

Versions verified on 2026-09-07: GenosSwift 3.0.0-alpha03, Genos Android 3.0.0-alpha06, Android Gradle Plugin 9.4.0, Kotlin Compose plugin 2.4.10, Gradle 9.7.1. Genos currently publishes these prerelease versions as its newest framework releases.

Independent business E2E tests belong in the project's separate QA repository. Building this skeleton does not constitute product completion, QA approval or deployment.
