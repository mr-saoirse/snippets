package life.drafter.drafterapp

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.interop.LocalUIViewController
import kotlinx.cinterop.ExperimentalForeignApi
import life.drafter.drafterapp.auth.AuthResponse
import platform.Foundation.NSError
import platform.UIKit.UIViewController
import cocoapods.GoogleSignIn.GIDSignIn
import cocoapods.GoogleSignIn.GIDSignInResult

@Composable
internal actual fun GoogleLoginButton(
    onResponse: (AuthResponse) -> Unit,
    modifier: Modifier
) {
    val uiViewController = LocalUIViewController.current

    GoogleButtonUI(
        modifier = modifier,
        onClick = { googleLogin(uiViewController, onResponse) }
    )
}

@OptIn(ExperimentalForeignApi::class)
private fun googleLogin(
    uiViewController: UIViewController,
    onLoggedIn: (AuthResponse) -> Unit
) {
    GIDSignIn.sharedInstance.signInWithPresentingViewController(uiViewController) { result, error ->
        when {
            result != null -> onLoggedIn(AuthResponse.Success(result.toGoogleAccount))
            error != null -> onLoggedIn(AuthResponse.Error(error.fullErrorMessage))
            else -> onLoggedIn(AuthResponse.Cancelled)
        }
    }
}

@OptIn(ExperimentalForeignApi::class)
private val GIDSignInResult.toGoogleAccount: GoogleAccount
    get() = GoogleAccount(
        idToken = user.idToken?.tokenString.orEmpty(),
        accessToken = user.accessToken.tokenString,
        profile = Profile(
            name = user.profile?.name.orEmpty(),
            familyName = user.profile?.familyName.orEmpty(),
            givenName = user.profile?.givenName.orEmpty(),
            email = user.profile?.email.orEmpty(),
            picture = user.profile?.imageURLWithDimension(100u)?.absoluteString
        ),
    )

private val NSError.fullErrorMessage: String
    get() {
        val underlyingErrors = underlyingErrors.joinToString(", ") { it.toString() }
        val recoveryOptions = localizedRecoveryOptions?.joinToString(", ") { it.toString() }

        return listOfNotNull(
            "code: $code",
            domain?.let { "domain: $domain" },
            "description: $localizedDescription",
            localizedFailureReason?.let { "reason: $localizedFailureReason" },
            localizedRecoverySuggestion?.let { "suggestion: $localizedRecoverySuggestion" },
            "underlyingErrors: $underlyingErrors",
            "recoveryOptions: $recoveryOptions".takeIf { recoveryOptions != null },
        ).joinToString("\n")
    }