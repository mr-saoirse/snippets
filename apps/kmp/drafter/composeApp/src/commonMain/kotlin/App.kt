
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import com.mmk.kmpauth.google.GoogleAuthCredentials
import com.mmk.kmpauth.google.GoogleAuthProvider
import com.mmk.kmpauth.google.GoogleButtonUiContainer
import com.mmk.kmpauth.uihelper.google.GoogleSignInButton
import org.jetbrains.compose.ui.tooling.preview.Preview

@Composable
@Preview
fun App() {
    var authReady by remember { mutableStateOf(false) }
    //the app in the google-services.json has a client id (type 3, web oauth) which we use for that value
    LaunchedEffect(Unit){
        GoogleAuthProvider.create(credentials = GoogleAuthCredentials(serverId = "519161200913-tnl45smv27vrq28ma1pajv9sdaia4abu.apps.googleusercontent.com"))
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
}