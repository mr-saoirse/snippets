package life.drafter.drafterapp

import androidx.compose.runtime.Composable
import life.drafter.drafterapp.auth.AuthResponse
import androidx.compose.ui.Modifier

@Composable
internal expect fun GoogleLoginButton(
    onResponse: (AuthResponse) -> Unit,
    modifier: Modifier = Modifier
)