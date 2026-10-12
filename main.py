import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import platform

SCAM_KEYWORDS = [
    r"lottery", r"won \d+", r"apk", r"pan card", r"electricity bill",
    r"power cut", r"free recharge", r"kyc update", r"gift card", r"blocked",
    r"parisu", r"panam", r"vetri", r"kadan", r"velai"
]
SUSPICIOUS_DOMAINS = [r"\.ru", r"\.xyz", r"\.top", r"bit\.ly", r"tinyurl", r"t\.me", r"\.apk"]

class KavachShield(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=12, spacing=10)

        root.add_widget(Label(
            text="🛡️ KAVACH: CYBER FRAUD SHIELD",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=40,
            color=(0.1, 0.6, 0.9, 1)
        ))

        self.txt_input = TextInput(
            hint_text="Paste suspicious SMS, caller link, or payment request...",
            multiline=True,
            size_hint_y=0.25
        )
        root.add_widget(self.txt_input)

        btn_scan = Button(
            text="SCAN MESSAGE / URL",
            background_color=(0.2, 0.5, 0.8, 1),
            size_hint_y=None,
            height=45
        )
        btn_scan.bind(on_press=self.scan_threats)
        root.add_widget(btn_scan)

        btn_upi = Button(
            text="UPI / GPAY SAFETY RULES",
            background_color=(0.2, 0.7, 0.4, 1),
            size_hint_y=None,
            height=45
        )
        btn_upi.bind(on_press=self.show_upi_rules)
        root.add_widget(btn_upi)

        scroll = ScrollView(size_hint_y=0.35)
        self.lbl_result = Label(
            text="Scan results will appear here.",
            text_size=(Window.width - 30, None),
            halign="left",
            valign="top",
            size_hint_y=None
        )
        self.lbl_result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        scroll.add_widget(self.lbl_result)
        root.add_widget(scroll)

        actions = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=50)

        btn_call = Button(
            text="DIAL 1930 (HELPLINE)",
            background_color=(0.9, 0.2, 0.2, 1),
            font_size="12sp"
        )
        btn_call.bind(on_press=self.dial_emergency)
        actions.add_widget(btn_call)

        btn_report = Button(
            text="GOVT PORTAL (CHAKSHU)",
            background_color=(0.9, 0.5, 0.1, 1),
            font_size="12sp"
        )
        btn_report.bind(on_press=self.open_portal)
        actions.add_widget(btn_report)

        root.add_widget(actions)
        return root

    def scan_threats(self, instance):
        text = self.txt_input.text.strip().lower()
        if not text:
            self.lbl_result.text = "Please paste text or link to scan."
            return

        threats = []
        score = 0

        for pattern in SCAM_KEYWORDS:
            if re.search(pattern, text):
                score += 35
                threats.append(f"• Scam keyword: '{pattern}'")

        if re.search(r"https?://", text) or ".apk" in text:
            score += 25
            threats.append("• Contains external link or APK install lure.")
            for domain in SUSPICIOUS_DOMAINS:
                if re.search(domain, text):
                    score += 40
                    threats.append(f"• Suspicious domain flag: '{domain}'")

        self.lbl_result.markup = True
        if score >= 50:
            self.lbl_result.text = (
                f"[color=ff4444]DANGER: HIGH FRAUD RISK ({min(score, 100)}%)[/color]\n\n"
                + "\n".join(threats) +
                "\n\nDO NOT click links or enter UPI PIN. Dial 1930 if funds were stolen."
            )
        else:
            self.lbl_result.text = "[color=44ff44]STATUS: SAFE[/color]\n\nNo common phishing triggers detected."

    def show_upi_rules(self, instance):
        self.lbl_result.markup = True
        self.lbl_result.text = (
            "[color=ffff44]CRITICAL UPI RULES:[/color]\n\n"
            "1. You NEVER enter a PIN to receive money on GPay/PhonePe.\n"
            "2. Scanning any QR code always DEBITS money from your account.\n"
            "3. Any caller claiming to give a 'refund' via payment request is a scammer."
        )

    def dial_emergency(self, instance):
        if platform == "android":
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            intent = Intent(Intent.ACTION_DIAL)
            intent.setData(Uri.parse("tel:1930"))
            PythonActivity.mActivity.startActivity(intent)
        else:
            import webbrowser
            webbrowser.open("tel:1930")

    def open_portal(self, instance):
        import webbrowser
        webbrowser.open("https://sancharsaathi.gov.in/sfc/")

if __name__ == "__main__":
    KavachShield().run()
