//import SwiftUI
//
//import FirebaseCore
////import GoogleSignInSwift
////import GoogleSignIn
//
//@main
//struct iOSApp: App {
//    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate
//	var body: some Scene {
//		WindowGroup {
//			ContentView()
//		}
//	}
//}
//
//class AppDelegate: NSObject, UIApplicationDelegate {
//    func application(_ application: UIApplication,
//                     didFinishLaunchingWithOptions launchOptions:
//                     [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
//
//        FirebaseApp.configure()
//
//
//        return true
//    }
//}

import SwiftUI
import shared
import GoogleSignIn

class AppDelegate: NSObject, UIApplicationDelegate {

    func application(
      _ app: UIApplication,
      open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]
    ) -> Bool {
      var handled: Bool

      handled = GIDSignIn.sharedInstance.handle(url)
      if handled {
        return true
      }

      // Handle other custom URL types.

      // If not handled by this app, return false.
      return false
    }


}

@main
struct iOSApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate

   var body: some Scene {
      WindowGroup {
            ContentView().onOpenURL(perform: { url in
                GIDSignIn.sharedInstance.handle(url)
            })
      }
   }
}
