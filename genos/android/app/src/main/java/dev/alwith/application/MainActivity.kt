package dev.alwith.application

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import genos.ui.activity.BaseActivity

class MainActivity : BaseActivity() {
    @Composable
    override fun Content() {
        Text("App")
    }
}
