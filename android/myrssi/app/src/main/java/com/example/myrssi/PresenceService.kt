package com.example.myrssi

import android.app.*
import android.content.Context
import android.content.Intent
import android.net.wifi.WifiManager
import android.os.*
import android.util.Log
import androidx.core.app.NotificationCompat

class PresenceService : Service() {

    companion object {
        private const val RSSI_UNAVAILABLE = -127
    }

    private lateinit var wifiManager: WifiManager

    private val detector = PresenceDetector()
    private val handler = Handler(Looper.getMainLooper())
    private val intervalMs = 1000L / 10

    private val loop = object : Runnable {
        override fun run() {
            @Suppress("DEPRECATION")
            val raw = wifiManager.connectionInfo.rssi
            val rssi = if (raw == RSSI_UNAVAILABLE) null else raw
            val state = detector.update(rssi)
            Log.d("Presence", "rssi=$rssi var=%.2f motion=%.2f state=%s".format(detector.lastVariance, detector.lastMotion, state))
            updateNotification(state)
            handler.postDelayed(this, intervalMs)

        }
    }

    override fun onCreate() {
        super.onCreate()
        wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        startForeground(1, buildNotification("starting"))
        handler.post(loop)
    }

    override fun onDestroy() {
        handler.removeCallbacks(loop)
        super.onDestroy()
    }

    private fun buildNotification(state: String): Notification {
        val channelId = "presence_channel"
        val channel = NotificationChannel(channelId, "Presence", NotificationManager.IMPORTANCE_LOW)
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)

        return NotificationCompat.Builder(this, channelId)
            .setContentTitle("Presence: $state")
            .setSmallIcon(android.R.drawable.ic_menu_compass)
            .build()
    }

    private fun updateNotification(state: String) {
        getSystemService(NotificationManager::class.java).notify(1, buildNotification(state))
    }

    override fun onBind(intent: Intent): IBinder? = null
}