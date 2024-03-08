from burp import IBurpExtender
from burp import ITab, IExtensionStateListener
from javax import swing
from java.awt import Dimension, BorderLayout
from java.lang import Runnable, Thread

import subprocess

class BurpExtender(IBurpExtender, ITab, IExtensionStateListener):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("nmap4burp")
        print("== Nmap 4 Burp ==")
        print("Stretching some legs...")
        print("Good to go!")

        callbacks.registerExtensionStateListener(self)
        self.author = "Jai Sharma"
        self.version = "1.0.0"
        self.github_link = "https://github.com/ja1sh/Nmap4Burp"

        self._tab = swing.JPanel()
        self._tab.setLayout(BorderLayout())

        topPanel = swing.JPanel()
        topPanel.setLayout(swing.BoxLayout(topPanel, swing.BoxLayout.Y_AXIS))
        self._nmapPathLabel = swing.JLabel("Enter the path to 'nmap' binary:")
        self._nmapPathField = swing.JTextField()
        self._nmapPathField.setMaximumSize(Dimension(32767, self._nmapPathField.getPreferredSize().height))
        self._nmapPathField.setColumns(20)
        self._targetLabel = swing.JLabel("Enter the target IP or domain:")
        self._targetField = swing.JTextField()
        self._targetField.setMaximumSize(Dimension(32767, self._targetField.getPreferredSize().height))
        self._targetField.setColumns(20)
        self._customCommandLabel = swing.JLabel("Enter custom Nmap command:")
        self._customCommandField = swing.JTextField()
        self._customCommandField.setMaximumSize(Dimension(32767, self._customCommandField.getPreferredSize().height))
        self._customCommandField.setColumns(20)
        self._runScanButton = swing.JButton("Run Nmap Scan", actionPerformed=self.runNmapScan)

        topPanel.add(self._nmapPathLabel)
        topPanel.add(self._nmapPathField)
        topPanel.add(self._targetLabel)
        topPanel.add(self._targetField)
        topPanel.add(self._customCommandLabel)
        topPanel.add(self._customCommandField)
        topPanel.add(self._runScanButton)

        self._scrollPane = swing.JScrollPane()
        self._textArea = swing.JTextArea()
        self._textArea.setEditable(False)
        self._scrollPane.setViewportView(self._textArea)

        self._bottomRightPanel = swing.JPanel()
        self._bottomRightPanel.setLayout(BorderLayout())
        self._bottomRightPanel.add(self._scrollPane, BorderLayout.CENTER)

        self._authorLabel = swing.JLabel("Author: " + self.author + " | Version: " + self.version + " | GitHub: "+self.github_link)
        self._bottomRightPanel.add(self._authorLabel, BorderLayout.SOUTH)

        self._tab.add(topPanel, BorderLayout.NORTH)
        self._tab.add(self._bottomRightPanel, BorderLayout.SOUTH)

        callbacks.addSuiteTab(self)


    def runNmapScan(self, event):
        nmap_path = self._nmapPathField.getText()
        target = self._targetField.getText()
        custom_command = self._customCommandField.getText()

        if not nmap_path:
            self.printToConsole("Please enter the path to 'nmap' binary.")
            return
        if not target:
            self.printToConsole("Please enter the target IP or domain.")
            return

        if custom_command:
            command = [nmap_path] + custom_command.split() + [target]
        else:
            command = [nmap_path, '-p', '1-1000', target]

        self.printToConsole("Nmap Command: {}".format(" ".join(command)))  # Print the Nmap command
        Thread(NmapScanner(command, self)).start()


    def printToConsole(self, message):
        self._callbacks.issueAlert(message)
        self._callbacks.getStderr().write(message + '\n')
        self._textArea.append(message + '\n')

    def getTabCaption(self):
        return "Nmap 4 Burp"

    def getUiComponent(self):
        return self._tab

    def extensionUnloaded(self):
        self.printExtensionInfo()

    def printExtensionInfo(self):
        info = (
            "Extension Name: {}\n"
            "Author: {}\n"
            "Social Media Links:\n{}\n"
            "Version: {}\n"
            "GitHub Link: {}\n"
        ).format(
            self._callbacks.getExtensionName(),
            self.author,
            "\n".join(["{}: {}".format(platform, link) for platform, link in self.social_media_links.items()]),
            self.version,
            self.github_link
        )
        self._textArea.setText(info)
        self.printToConsole("Extension information displayed on the tab.")

class NmapScanner(Runnable):
    def __init__(self, command, burp_extender):
        self._command = command
        self._burp_extender = burp_extender

    def run(self):
        try:
            process = subprocess.Popen(self._command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                line = process.stdout.readline().decode('utf-8')
                if not line:
                    break
                self._burp_extender.printToConsole(line)

            remaining_output = process.stdout.read().decode('utf-8')
            if remaining_output:
                self._burp_extender.printToConsole(remaining_output)

            process.wait()
            self._burp_extender.printToConsole("Nmap scan completed successfully.")
        except subprocess.CalledProcessError as e:
            self._burp_extender.printToConsole("Error running nmap: {}".format(e))
            self._burp_extender.printToConsole(e.stderr.decode('utf-8'))
