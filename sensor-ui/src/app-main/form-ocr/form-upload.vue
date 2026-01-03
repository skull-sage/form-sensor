<template>
  <a-section>
    <div class="q-pa-md">
      <div class="row justify-center">
        <div class="col-12 col-md-10 col-lg-8">
          <!-- Upload Card -->
          <q-card class="q-mb-lg" v-if="!processResult">
            <q-card-section>
              <div class="text-h5 q-mb-md">
                <q-icon name="scanner" class="q-mr-sm" />
                Upload Form for OCR Processing
              </div>

              <q-file
                v-model="selectedFile"
                label="Select PDF file"
                accept=".pdf"
                outlined
                clearable
                :rules="[
                  (val: File | null) => !!val || 'Please select a PDF file',
                  (val: File | null) => (val && val.type === 'application/pdf') || 'Only PDF files are allowed',
                  (val: File | null) => (val && val.size <= 20971520) || 'File size must be less than 20MB'
                ]"
                @update:model-value="onFileSelected"
              >
                <template v-slot:prepend>
                  <q-icon name="attach_file" />
                </template>
                <template v-slot:hint>
                  Upload a scanned form in PDF format (max 20MB)
                </template>
              </q-file>

              <!-- OCR Options -->
              <q-expansion-item
                class="q-mt-md"
                label="OCR Options"
                icon="settings"
                header-class="bg-grey-2"
              >
                <q-card>
                  <q-card-section>
                    <div class="q-gutter-md">
                      <q-select
                        v-model="ocrOptions.language"
                        :options="languageOptions"
                        label="Language"
                        outlined
                        dense
                        emit-value
                        map-options
                      />

                      <q-toggle
                        v-model="ocrOptions.enable_correction"
                        label="Enable Perspective Correction"
                        color="primary"
                      />

                      <q-toggle
                        v-model="ocrOptions.enable_segment_detection"
                        label="Enable Form Segment Detection"
                        color="primary"
                      />

                      <q-toggle
                        v-model="ocrOptions.use_gpu"
                        label="Use GPU Acceleration (if available)"
                        color="primary"
                      />

                      <q-slider
                        v-model="ocrOptions.confidence_threshold"
                        :min="0"
                        :max="1"
                        :step="0.05"
                        label
                        label-always
                        :label-value="`Confidence: ${ocrOptions.confidence_threshold}`"
                        color="primary"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </q-expansion-item>

              <div class="q-mt-md row justify-end">
                <q-btn
                  color="primary"
                  label="Process Form"
                  icon="play_arrow"
                  :loading="processing"
                  :disable="!selectedFile"
                  @click="processForm"
                />
              </div>
            </q-card-section>
          </q-card>

          <!-- Processing Result -->
          <div v-if="processResult">
            <q-card class="q-mb-md">
              <q-card-section class="bg-primary text-white">
                <div class="row items-center justify-between">
                  <div class="text-h6">
                    <q-icon name="check_circle" class="q-mr-sm" />
                    Form Processing Complete
                  </div>
                  <q-btn
                    flat
                    round
                    icon="close"
                    @click="resetProcessing"
                  >
                    <q-tooltip>Process another form</q-tooltip>
                  </q-btn>
                </div>
                <div class="text-caption">Form ID: {{ processResult.form_id }}</div>
                <div class="text-caption">Processing Time: {{ processResult.processing_time }}s</div>
                <div class="text-caption">Total Images Processed: {{ processResult.page_count }}</div>
              </q-card-section>
            </q-card>

            <!-- Extracted Form Fields -->
            <q-card
              v-for="(page, pageIndex) in processResult.pages"
              :key="page.page_number"
              class="q-mb-md"
            >
              <q-card-section>
                <div class="text-h6 q-mb-md">
                  <q-icon name="description" color="primary" class="q-mr-sm" />
                  Form Image {{ page.page_number }}
                  <q-chip
                    color="info"
                    text-color="white"
                    size="sm"
                    class="q-ml-sm"
                  >
                    {{ page.form_fields?.length || 0 }} fields detected
                  </q-chip>
                </div>

                <!-- Form Fields as Key-Value Pairs -->
                <div v-if="page.form_fields && page.form_fields.length > 0">
                  <q-list bordered separator class="rounded-borders">
                    <q-item
                      v-for="(field, index) in page.form_fields"
                      :key="index"
                      class="q-py-md"
                    >
                      <q-item-section>
                        <q-item-label class="text-subtitle1 text-weight-medium text-grey-8">
                          {{ field.label }}
                        </q-item-label>
                        <q-item-label class="text-body1 q-mt-xs">
                          {{ field.value || '(empty)' }}
                        </q-item-label>
                        <q-item-label caption class="q-mt-xs">
                          Confidence: {{ (field.confidence * 100).toFixed(1) }}% | Layout: {{ field.layout }}
                        </q-item-label>
                      </q-item-section>
                      <q-item-section side top>
                        <q-chip
                          :color="getConfidenceColor(field.confidence)"
                          text-color="white"
                          size="sm"
                        >
                          {{ (field.confidence * 100).toFixed(0) }}%
                        </q-chip>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </div>

                <!-- No Fields Detected Message -->
                <div v-else class="text-center q-pa-md bg-grey-2 rounded-borders">
                  <q-icon name="info" size="md" color="grey-6" />
                  <div class="text-body2 text-grey-7 q-mt-sm">
                    No form fields detected in this image
                  </div>
                </div>
              </q-card-section>
            </q-card>

            <!-- Actions -->
            <div class="row q-gutter-sm justify-center q-mt-md">
              <q-btn
                color="primary"
                label="Process Another Form"
                icon="upload_file"
                @click="resetProcessing"
              />
              <q-btn
                color="secondary"
                label="View All Forms"
                icon="list"
                :to="{name: 'form-ocr.list'}"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </a-section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// API base URL
const API_BASE_URL = 'http://localhost:8000'

// Types
interface TextRegion {
  text: string
  confidence: number
  bounding_box: number[][]
}

interface FormField {
  label: string
  value: string | null
  layout: string
  confidence: number
}

interface PageResult {
  page_number: number
  original_image: string
  corrected_image: string
  correction_applied: boolean
  text_regions: TextRegion[]
  form_fields: FormField[]
}

interface FormProcessResponse {
  form_id: string
  page_count: number
  processing_time: number
  pages: PageResult[]
  metadata: Record<string, any>
}

// Language options
const languageOptions = [
  { label: 'English', value: 'en' },
  { label: 'Chinese', value: 'ch' },
  { label: 'French', value: 'fr' },
  { label: 'German', value: 'german' },
  { label: 'Korean', value: 'korean' },
  { label: 'Japanese', value: 'japan' }
]

// Reactive data
const selectedFile = ref<File | null>(null)
const processing = ref(false)
const processResult = ref<FormProcessResponse | null>(null)

const ocrOptions = ref({
  language: 'en',
  use_gpu: false,
  enable_correction: true,
  confidence_threshold: 0.5,
  enable_segment_detection: true
})

// File selection handler
const onFileSelected = (file: File | null) => {
  if (file) {
    console.log('File selected:', file.name, file.size, 'bytes')
  }
}

// Process form
const processForm = async () => {
  if (!selectedFile.value) {
    $q.notify({
      type: 'negative',
      message: 'Please select a PDF file'
    })
    return
  }

  processing.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('language', ocrOptions.value.language)
    formData.append('use_gpu', String(ocrOptions.value.use_gpu))
    formData.append('enable_correction', String(ocrOptions.value.enable_correction))
    formData.append('confidence_threshold', String(ocrOptions.value.confidence_threshold))
    formData.append('enable_segment_detection', String(ocrOptions.value.enable_segment_detection))

    const response = await fetch(`${API_BASE_URL}/form-ocr/process-form`, {
      method: 'POST',
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      processResult.value = data

      $q.notify({
        type: 'positive',
        message: 'Form processed successfully',
        caption: `Form ID: ${data.form_id}`
      })
    } else {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }
  } catch (error) {
    console.error('Error processing form:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to process form',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    processing.value = false
  }
}

// Reset processing
const resetProcessing = () => {
  selectedFile.value = null
  processResult.value = null
}

// Get confidence color
const getConfidenceColor = (confidence: number): string => {
  if (confidence >= 0.8) return 'positive'
  if (confidence >= 0.6) return 'warning'
  return 'negative'
}
</script>

<style scoped>
.rounded-borders {
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}
</style>
