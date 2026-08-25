package com.example.myrssi

class PresenceDetector (
    private val window: Int = 30,
    private val absentVar: Double = 0.3,
    private val motionDelta: Double = 0.25,
    private val hysteresis: Int = 3
) {
    private val buf = ArrayDeque<Double>()

    var state: String = "absent"
        private set

    var lastVariance: Double = 0.0
        private set

    var lastMotion: Double = 0.0
        private set

    private var pending: String? = null
    private var pendingCount = 0

    fun update(rssi: Int?): String {
        if (rssi == null) return state

        buf.addLast(rssi.toDouble())

        if (buf.size > window) buf.removeFirst()
        if (buf.size < 4) return state

        val mean = buf.average()
        val variance = buf.sumOf{ (it - mean) * (it - mean) } / buf.size
        val motion = buf.zipWithNext { a, b -> kotlin.math.abs(b - a) }.average()

        lastVariance = variance
        lastMotion = motion

        val newState = when {
            variance < absentVar -> "absent"
            motion > motionDelta -> "moving"
            else -> "still"
        }

        if (newState == pending) pendingCount++ else {
            pending = newState
            pendingCount = 1
        }

        if (pendingCount >= hysteresis) state = newState

        return state
    }
}