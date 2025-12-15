<template>
  <a-section>
    <div class="q-pa-md">
      <div class="row q-gutter-md">
        <!-- Create New Sensor Card -->
        <div class="col-12 col-md-5">
          <q-card class="q-pa-md">
            <q-card-section>
              <div class="text-h6 q-mb-md">Create New Text Sensor</div>

              <q-form @submit="createSensor" class="q-gutter-md">
                <q-input
                  v-model="newSensor.nameId"
                  label="Sensor Name ID"
                  hint="Alphanumeric, hyphens, and underscores only"
                  :rules="[
                    val => !!val || 'Name ID is required',
                    val => val.length <= 100 || 'Name ID too long (max 100 chars)',
                    val => /^[a-zA-Z0-9_-]+$/.test(val) || 'Only letters, numbers, hyphens, and underscores allowed'
                  ]"
                  outlined
                  dense
                />

                <q-input
                  v-model="newSensor.text"
                  label="Text Content"
                  hint="Enter multiple paragraphs separated by newlines"
                  type="textarea"
                  rows="6"
                  :rules="[
                    val => !!val || 'Text content is required',
                    val => val.trim().length > 0 || 'Text cannot be empty',
                    val => val.length <= 10000 || 'Text too long (max 10,000 chars)'
                  ]"
                  outlined
                />

                <div class="row justify-end">
                  <q-btn
                    type="submit"
                    color="primary"
                    label="Create Sensor"
                    :loading="creating"
                    :disable="!newSensor.nameId || !newSensor.text"
                  />
                </div>
              </q-form>
            </q-card-section>
          </q-card>
        </div>

        <!-- Sensors List -->
        <div class="col-12 col-md-6">
          <q-card class="q-pa-md">
            <q-card-section>
              <div class="row items-center justify-between q-mb-md">
                <div class="text-h6">Text Sensors ({{ sensors.length }})</div>
                <q-btn
                  flat
                  round
                  color="primary"
                  icon="refresh"
                  @click="loadSensors"
                  :loading="loading"
                  size="sm"
                />
              </div>

              <div v-if="(loading || bulkCreating) && sensors.length === 0" class="text-center q-pa-md">
                <q-spinner color="primary" size="2em" />
                <div class="q-mt-sm text-grey-6">
                  {{ bulkCreating ? 'Restoring sensors from browser storage...' : 'Loading sensors...' }}
                </div>
              </div>

              <div v-else-if="sensors.length === 0" class="text-center q-pa-md text-grey-6">
                <q-icon name="sensors" size="3em" class="q-mb-sm" />
                <div>No text sensors created yet</div>
                <div class="text-caption">Create your first sensor using the form on the left</div>
              </div>

              <div v-else class="q-gutter-sm">
                <q-card
                  v-for="sensor in sensors"
                  :key="sensor.nameId"
                  flat
                  bordered
                  class="sensor-card"
                >
                  <q-card-section class="q-pa-sm">
                    <div class="row items-start justify-between">
                      <div class="col">
                        <div class="text-weight-bold text-primary">{{ sensor.nameId }}</div>
                        <div class="text-caption text-grey-6 q-mt-xs">
                          {{ getParagraphCount(sensor.text) }} paragraphs
                        </div>
                        <div class="text-body2 q-mt-sm text-truncate-3">
                          {{ sensor.text }}
                        </div>
                      </div>
                      <div class="col-auto q-ml-sm">
                        <div class="q-gutter-xs">
                          <q-btn
                            flat
                            round
                            color="primary"
                            icon="content_copy"
                            size="sm"
                            @click="copySensorText(sensor.text, sensor.nameId)"
                          >
                            <q-tooltip>Copy sensor text</q-tooltip>
                          </q-btn>
                          <q-btn
                            flat
                            round
                            color="negative"
                            icon="delete"
                            size="sm"
                            @click="deleteSensor(sensor.nameId)"
                            :loading="deleting === sensor.nameId"
                          >
                            <q-tooltip>Delete sensor</q-tooltip>
                          </q-btn>
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </a-section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// API base URL - adjust as needed
const API_BASE_URL = 'http://localhost:8000'

// Browser storage key
const STORAGE_KEY = 'semantic-sensors-storage'

// Reactive data
const sensors = ref<Array<{ nameId: string; text: string }>>([])
const loading = ref(false)
const creating = ref(false)
const deleting = ref<string | null>(null)
const bulkCreating = ref(false)
const hasInitialized = ref(false)

const newSensor = ref({
  nameId: '',
  text: ''
})

// Helper function to count paragraphs
const getParagraphCount = (text: string): number => {
  return text.split('\n').filter(p => p.trim().length > 0).length
}

// Browser storage functions
const saveSensorToStorage = (nameId: string, text: string) => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    const sensors = stored ? JSON.parse(stored) : {}
    sensors[nameId] = text
    localStorage.setItem(STORAGE_KEY, JSON.stringify(sensors))
  } catch (error) {
    console.error('Error saving to localStorage:', error)
  }
}

const removeSensorFromStorage = (nameId: string) => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      const sensors = JSON.parse(stored)
      delete sensors[nameId]
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sensors))
    }
  } catch (error) {
    console.error('Error removing from localStorage:', error)
  }
}

const getStoredSensors = (): Record<string, string> => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    return stored ? JSON.parse(stored) : {}
  } catch (error) {
    console.error('Error reading from localStorage:', error)
    return {}
  }
}

// Bulk create sensors from browser storage
const bulkCreateFromStorage = async () => {
  const storedSensors = getStoredSensors()

  if (Object.keys(storedSensors).length === 0) {
    return // No stored sensors to create
  }

  bulkCreating.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/bulk-create-sensors`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sensors: storedSensors
      })
    })

    if (response.ok) {
      const data = await response.json()

      if (data.created.length > 0) {
        $q.notify({
          type: 'positive',
          message: `Restored ${data.created.length} sensor(s) from browser storage`,
          caption: data.created.join(', ')
        })
      }

      if (data.skipped.length > 0) {
        console.log(`Skipped existing sensors: ${data.skipped.join(', ')}`)
      }

      if (data.failed.length > 0) {
        $q.notify({
          type: 'warning',
          message: `Failed to restore ${data.failed.length} sensor(s)`,
          caption: data.failed.join(', ')
        })
      }
    } else {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }
  } catch (error) {
    console.error('Error bulk creating sensors:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to restore sensors from storage',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    bulkCreating.value = false
  }
}

// Load sensors from API
const loadSensors = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/text-sensors`)
    if (response.ok) {
      const data = await response.json()
      // Convert sensors object to array format
      sensors.value = Object.entries(data.sensors).map(([nameId, text]) => ({
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
    loading.value = false
  }
}

// Create new sensor
const createSensor = async () => {
  creating.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/create-text-sensor/${newSensor.value.nameId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: newSensor.value.text
      })
    })

    if (response.ok) {
      const data = await response.json()
      $q.notify({
        type: 'positive',
        message: 'Sensor created successfully',
        caption: `Created with ${data.paragraphs_count} paragraphs`
      })

      // Save to browser storage
      saveSensorToStorage(newSensor.value.nameId, newSensor.value.text)

      // Reset form
      newSensor.value = {
        nameId: '',
        text: ''
      }

      // Refresh the sensors list
      await loadSensors()
    } else {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }
  } catch (error) {
    console.error('Error creating sensor:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to create sensor',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    creating.value = false
  }
}

// Copy sensor text to clipboard
const copySensorText = async (text: string, nameId: string) => {
  try {
    await navigator.clipboard.writeText(text)
    $q.notify({
      type: 'positive',
      message: 'Text copied to clipboard',
      caption: `Sensor: ${nameId}`,
      timeout: 2000
    })
  } catch (error) {
    // Fallback for browsers that don't support clipboard API
    try {
      const textArea = document.createElement('textarea')
      textArea.value = text
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      document.execCommand('copy')
      textArea.remove()

      $q.notify({
        type: 'positive',
        message: 'Text copied to clipboard',
        caption: `Sensor: ${nameId}`,
        timeout: 2000
      })
    } catch (fallbackError) {
      console.error('Failed to copy text:', fallbackError)
      $q.notify({
        type: 'negative',
        message: 'Failed to copy text',
        caption: 'Clipboard access not available'
      })
    }
  }
}

// Delete sensor
const deleteSensor = async (nameId: string) => {
  $q.dialog({
    title: 'Confirm Delete',
    message: `Are you sure you want to delete the sensor "${nameId}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    deleting.value = nameId
    try {
      const response = await fetch(`${API_BASE_URL}/text-sensor/${nameId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        $q.notify({
          type: 'positive',
          message: 'Sensor deleted successfully'
        })

        // Remove from browser storage
        removeSensorFromStorage(nameId)

        // Refresh the sensors list
        await loadSensors()
      } else {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }
    } catch (error) {
      console.error('Error deleting sensor:', error)
      $q.notify({
        type: 'negative',
        message: 'Failed to delete sensor',
        caption: error instanceof Error ? error.message : 'Unknown error'
      })
    } finally {
      deleting.value = null
    }
  })
}

// Initialize component - restore from storage and load sensors
const initializeComponent = async () => {
  if (!hasInitialized.value) {
    hasInitialized.value = true

    // First, try to bulk create sensors from browser storage
    await bulkCreateFromStorage()
  }

  // Then load all sensors from API
  await loadSensors()
}

// Load sensors on component mount
onMounted(() => {
  initializeComponent()
})
</script>

<style scoped>
.sensor-card {
  transition: all 0.2s ease;
}

.sensor-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.text-truncate-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
  max-height: 4.2em;
}
</style>
