<template>
  <a-section>
    <div class="q-pa-md">
      <div class="row justify-center">
        <div class="col-12 col-md-8 col-lg-6">
          <q-card class="q-pa-md">
            <q-card-section>
              <div class="text-h6 q-mb-md">Test Text Field Verification</div>

              <q-form @submit="verifyText" class="q-gutter-md">
                <!-- Sensor Selection -->
                <q-select
                  v-model="selectedSensor"
                  :options="sensorOptions"
                  label="Select Text Sensor"
                  hint="Choose a sensor to test against"
                  outlined
                  dense
                  :loading="loadingSensors"
                  :rules="[val => !!val || 'Please select a sensor']"
                  @focus="loadSensors"
                >
                  <template v-slot:no-option>
                    <q-item>
                      <q-item-section class="text-grey">
                        {{ loadingSensors ? 'Loading sensors...' : 'No sensors available. Create one first.' }}
                      </q-item-section>
                    </q-item>
                  </template>
                </q-select>

                <!-- Text Input -->
                <q-input
                  v-model="testText"
                  label="Text to Verify"
                  hint="Enter text to check similarity against the selected sensor"
                  type="textarea"
                  rows="4"
                  :rules="[
                    val => !!val || 'Text is required',
                    val => val.trim().length > 0 || 'Text cannot be empty',
                    val => val.length <= 5000 || 'Text too long (max 5,000 chars)'
                  ]"
                  outlined
                />

                <!-- Submit Button -->
                <div class="row justify-center">
                  <q-btn
                    type="submit"
                    color="primary"
                    label="Verify Text"
                    :loading="verifying"
                    :disable="!selectedSensor || !testText"
                    class="q-px-xl"
                  />
                </div>
              </q-form>
            </q-card-section>
          </q-card>

          <!-- Results Card -->
          <q-card v-if="result" class="q-mt-md q-pa-md">
            <q-card-section>
              <div class="text-h6 q-mb-md">Verification Results</div>

              <!-- Confidence Score Display -->
              <div class="row items-center q-mb-md">
                <div class="col-auto">
                  <div class="text-subtitle1">Confidence Score:</div>
                </div>
                <div class="col q-ml-md">
                  <q-linear-progress
                    :value="result.confidence_score"
                    size="20px"
                    :color="getConfidenceColor(result.confidence_score)"
                    class="q-mr-sm"
                  />
                </div>
                <div class="col-auto">
                  <q-chip
                    :color="getConfidenceColor(result.confidence_score)"
                    text-color="white"
                    :label="`${(result.confidence_score * 100).toFixed(1)}%`"
                  />
                </div>
              </div>

              <!-- Confidence Interpretation -->
              <q-banner
                :class="`bg-${getConfidenceColor(result.confidence_score)}-1 text-${getConfidenceColor(result.confidence_score)}-8`"
                class="q-mb-md"
              >
                <template v-slot:avatar>
                  <q-icon :name="getConfidenceIcon(result.confidence_score)" />
                </template>
                {{ getConfidenceMessage(result.confidence_score) }}
              </q-banner>

              <!-- Matched Paragraph -->
              <div class="q-mb-md">
                <div class="text-subtitle1 q-mb-sm">Best Matching Paragraph:</div>
                <q-card flat bordered class="bg-grey-1">
                  <q-card-section class="q-pa-sm">
                    <div class="text-body1">{{ result.matched_paragraph }}</div>
                  </q-card-section>
                </q-card>
              </div>

              <!-- Test Details -->
              <q-expansion-item
                icon="info"
                label="Test Details"
                class="bg-grey-2"
              >
                <q-card>
                  <q-card-section class="q-pa-sm">
                    <div class="text-caption">
                      <div><strong>Sensor:</strong> {{ selectedSensor?.label }}</div>
                      <div><strong>Test Text:</strong> {{ testText }}</div>
                      <div><strong>Threshold (Reference):</strong> 60% (0.6)</div>
                      <div><strong>Match Status:</strong>
                        <q-chip
                          :color="result.confidence_score >= 0.6 ? 'positive' : 'warning'"
                          text-color="white"
                          size="sm"
                          :label="result.confidence_score >= 0.6 ? 'Above Threshold' : 'Below Threshold'"
                        />
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </q-expansion-item>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </a-section>
</template>
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// API base URL - adjust as needed
const API_BASE_URL = 'http://localhost:8000'

// Types
interface SensorOption {
  label: string
  value: string
}

interface VerificationResult {
  confidence_score: number
  matched_paragraph: string
}

// Reactive data
const selectedSensor = ref<SensorOption | null>(null)
const testText = ref('')
const result = ref<VerificationResult | null>(null)
const loadingSensors = ref(false)
const verifying = ref(false)
const availableSensors = ref<Array<{ nameId: string; text: string }>>([])

// Computed sensor options for the select dropdown
const sensorOptions = computed<SensorOption[]>(() => {
  return availableSensors.value.map(sensor => ({
    label: `${sensor.nameId} (${getParagraphCount(sensor.text)} paragraphs)`,
    value: sensor.nameId
  }))
})

// Helper function to count paragraphs
const getParagraphCount = (text: string): number => {
  return text.split('\n').filter(p => p.trim().length > 0).length
}

// Helper function to get confidence color based on score
const getConfidenceColor = (score: number): string => {
  if (score >= 0.8) return 'green'
  if (score >= 0.6) return 'orange'
  if (score >= 0.4) return 'amber'
  return 'red'
}

// Helper function to get confidence icon based on score
const getConfidenceIcon = (score: number): string => {
  if (score >= 0.8) return 'check_circle'
  if (score >= 0.6) return 'warning'
  if (score >= 0.4) return 'info'
  return 'error'
}

// Helper function to get confidence message based on score
const getConfidenceMessage = (score: number): string => {
  if (score >= 0.8) return 'Excellent match! The text is very similar to the stored content.'
  if (score >= 0.6) return 'Good match! The text shows significant similarity to the stored content.'
  if (score >= 0.4) return 'Moderate match. The text has some similarity to the stored content.'
  return 'Low match. The text shows little similarity to the stored content.'
}

// Load available sensors
const loadSensors = async () => {
  if (availableSensors.value.length > 0) return // Already loaded

  loadingSensors.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/text-sensors`)
    if (response.ok) {
      const data = await response.json()
      // Convert sensors object to array format
      availableSensors.value = Object.entries(data.sensors).map(([nameId, text]) => ({
        nameId,
        text: text as string
      }))
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('Error loading sensors:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load sensors',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    loadingSensors.value = false
  }
}

// Verify text against selected sensor
const verifyText = async () => {
  if (!selectedSensor.value) return

  verifying.value = true
  result.value = null

  try {
    const response = await fetch(`${API_BASE_URL}/text-sensor/${selectedSensor.value.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: testText.value
      })
    })

    if (response.ok) {
      const data = await response.json()
      result.value = {
        confidence_score: data.confidence_score,
        matched_paragraph: data.matched_paragraph
      }

      $q.notify({
        type: 'positive',
        message: 'Text verification completed',
        caption: `Confidence: ${(data.confidence_score * 100).toFixed(1)}%`
      })
    } else {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }
  } catch (error) {
    console.error('Error verifying text:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to verify text',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    verifying.value = false
  }
}
</script>

<style scoped>
.q-linear-progress {
  border-radius: 10px;
}

.q-chip {
  font-weight: bold;
}
</style>
