package life.drafter.drafterapp

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform