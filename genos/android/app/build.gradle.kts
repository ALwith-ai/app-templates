plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "dev.alwith.application"
    compileSdk = 37

    defaultConfig {
        applicationId = providers.gradleProperty("applicationId").get()
        minSdk = 34
        targetSdk = 37
        versionCode = 1
        versionName = "1.0.0"
    }

    buildFeatures {
        compose = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_27
        targetCompatibility = JavaVersion.VERSION_27
    }
}

dependencies {
    implementation("io.github.nyssance:genos:3.0.0-alpha08")
}
