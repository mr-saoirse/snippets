package life.drafter.drafterapp

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.mmk.kmpauth.google.GoogleAuthCredentials
import com.mmk.kmpauth.google.GoogleAuthProvider
import com.mmk.kmpauth.google.GoogleButtonUiContainer
import com.mmk.kmpauth.uihelper.google.GoogleSignInButton
import life.drafter.drafterapp.auth.AuthResponse
import org.jetbrains.compose.ui.tooling.preview.Preview

@Composable
@Preview
fun App() {
    var authReady by remember { mutableStateOf(false) }
    //the app in the google-services.json has a client id which we use for that value
    LaunchedEffect(Unit){
        GoogleAuthProvider.create(credentials = GoogleAuthCredentials(serverId = "610536849644-q6u3810lr7t62eqt1kcfgnot7m8l324g.apps.googleusercontent.com"))
        authReady = true
    }

    MaterialTheme{
        if (authReady) {
            //Screen
            Box(modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
                ) {
                GoogleButtonUiContainer(
                    onGoogleSignInResult = { googleUser ->
                        val tokenId = googleUser?.idToken
                        print("T: $tokenId")
                    }) {
                    GoogleSignInButton (onClick = { this.onClick() })
                }
            }
        }
    }
//    CompositionLocalProvider() {
//        MaterialTheme {
//            Column(
//                modifier = Modifier.fillMaxSize().background(Color.White),
//                verticalArrangement = Arrangement.Center,
//                horizontalAlignment = Alignment.CenterHorizontally
//            ) {
//                var userName: String by remember { mutableStateOf("") }
//
//                GoogleLoginButton(
//                    onResponse = {
//                        (it as? AuthResponse.Success)?.account?.profile?.name?.let { name ->
//                            userName = name
//                        }
//                    }
//                )
//
//                Spacer(modifier = Modifier.height(20.dp))
//
//                if (userName.isNotEmpty()) {
//                    Text("Welcome $userName")
//                }
//            }
//        }
//    }
}