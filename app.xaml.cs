/*protected async override void OnLaunched(LaunchActivatedEventArgs e)
{
    ...
    // Install the VCD
    try
    {
        StorageFile vcdStorageFile = await Package.Current.InstalledLocation.GetFileAsync(@"voicecommand.xml");
        await VoiceCommandDefinitionManager.InstallCommandDefinitionsFromStorageFileAsync(vcdStorageFile);
    }
    catch (Exception ex)
    {
        System.Diagnostics.Debug.WriteLine("There was an error registering the Voice Command Definitions", ex);
    }
}*/

using System;
using System.Collections.Generic;
using System.Linq;
using Windows.ApplicationModel;
using Windows.ApplicationModel.Activation;
using Windows.ApplicationModel.VoiceCommands;
using Windows.Media.SpeechRecognition;
using Windows.Storage;
using Windows.UI.Popups;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Navigation;

namespace LaunchApp
{
    /// <summary>
    /// Provides application-specific behavior to supplement the default Application class.
    /// </summary>
    sealed partial class App : Application
    {
        /// <summary>
        /// Initializes the singleton application object.  This is the first line of authored code
        /// executed, and as such is the logical equivalent of main() or WinMain().
        /// </summary>
        public App()
        {
            Microsoft.ApplicationInsights.WindowsAppInitializer.InitializeAsync(
                Microsoft.ApplicationInsights.WindowsCollectors.Metadata |
                Microsoft.ApplicationInsights.WindowsCollectors.Session);
            this.InitializeComponent();
            this.Suspending += OnSuspending;
        }

        /// <summary>
        /// Invoked when the application is launched normally by the end user.  Other entry points
        /// will be used such as when the application is launched to open a specific file.
        /// </summary>
        /// <param name="e">Details about the launch request and process.</param>
        protected async override void OnLaunched(LaunchActivatedEventArgs e)
        {

            if (System.Diagnostics.Debugger.IsAttached)
            {
                this.DebugSettings.EnableFrameRateCounter = true;
            }


            Frame rootFrame = Window.Current.Content as Frame;

            // Do not repeat app initialization when the Window already has content,
            // just ensure that the window is active
            if (rootFrame == null)
            {
                // Create a Frame to act as the navigation context and navigate to the first page
                rootFrame = new Frame();

                rootFrame.NavigationFailed += OnNavigationFailed;

                if (e.PreviousExecutionState == ApplicationExecutionState.Terminated)
                {
                    //TODO: Load state from previously suspended application
                }

                // Place the frame in the current Window
                Window.Current.Content = rootFrame;
            }

            if (rootFrame.Content == null)
            {
                // When the navigation stack isn't restored navigate to the first page,
                // configuring the new page by passing required information as a navigation
                // parameter
                rootFrame.Navigate(typeof(MainPage), e.Arguments);
            }
            // Ensure the current window is active
            Window.Current.Activate();

            // Install the VCD
            try
            {
                StorageFile vcdStorageFile = await Package.Current.InstalledLocation.GetFileAsync(@"voicecommands.xml");
                await VoiceCommandDefinitionManager.InstallCommandDefinitionsFromStorageFileAsync(vcdStorageFile);
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine("There was an error registering the Voice Command Definitions", ex);
            }
        }

        private void run_cmd(string cmd, string args)
        {
           ProcessStartInfo start = new ProcessStartInfo();
           start.FileName = cmd;//cmd is full path to python.exe
           start.Arguments = args;//args is path to .py file and any cmd line args
           start.UseShellExecute = false;
           start.RedirectStandardOutput = true;
           using(Process process = Process.Start(start))
           {
               using(StreamReader reader = process.StandardOutput)
               {
                   string result = reader.ReadToEnd();
                   Console.Write(result);
               }
           }
        }
        /// <summary>
        /// Invoked when the application is activated by some means other than normal launching.
        /// </summary>
        /// <param name="e">Event data for the event.</param>
        protected async override void OnActivated(IActivatedEventArgs e)
        {
            // Handle when app is launched by Cortana
            if (e.Kind == ActivationKind.VoiceCommand)
            {
                VoiceCommandActivatedEventArgs commandArgs = e as VoiceCommandActivatedEventArgs;
                SpeechRecognitionResult speechRecognitionResult = commandArgs.Result;

                string voiceCommandName = "Run";
                string textSpoken = speechRecognitionResult.Text;
                IReadOnlyList<string> recognizedVoiceCommandPhrases;

                System.Diagnostics.Debug.WriteLine("voiceCommandName: " + voiceCommandName);
                System.Diagnostics.Debug.WriteLine("textSpoken: " + textSpoken);

                MessageDialog messageDialog = new MessageDialog("");

                string path_to_python = 'C:\\Users\\Sergei\\AppData\\Local\\Programs\\Python\\Python36-32\\python.exe';
                string path_to_script = 'C:\\Users\\Sergei\\Documents\\NoseGoes\\run.py';

                switch (voiceCommandName)
                {
                    case "Run":
                        run_cmd(path_to_python, path_to_script)
                        break;

                    default:
                        messageDialog.Content = "Unknown command";
                        break;
                }

                await messageDialog.ShowAsync();
            }
        }

        /// <summary>
        /// Invoked when Navigation to a certain page fails
        /// </summary>
        /// <param name="sender">The Frame which failed navigation</param>
        /// <param name="e">Details about the navigation failure</param>
        private void OnNavigationFailed(object sender, NavigationFailedEventArgs e)
        {
            throw new Exception("Failed to load Page " + e.SourcePageType.FullName);
        }

        /// <summary>
        /// Invoked when application execution is being suspended.  Application state is saved
        /// without knowing whether the application will be terminated or resumed with the contents
        /// of memory still intact.
        /// </summary>
        /// <param name="sender">The source of the suspend request.</param>
        /// <param name="e">Details about the suspend request.</param>
        private void OnSuspending(object sender, SuspendingEventArgs e)
        {
            var deferral = e.SuspendingOperation.GetDeferral();
            //TODO: Save application state and stop any background activity
            deferral.Complete();
        }
    }
}
