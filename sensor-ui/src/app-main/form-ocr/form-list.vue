<template>
  <a-section>
    <div class="q-pa-md">
      <div class="row justify-center">
        <div class="col-12 col-lg-10">
          <!-- Header -->
          <div class="row items-center justify-between q-mb-md">
            <div class="text-h5">
              <q-icon name="folder" class="q-mr-sm" />
              Form Library
            </div>
            <div class="q-gutter-sm">
              <q-btn
                flat
                round
                color="primary"
                icon="refresh"
                @click="loadForms"
                :loading="loading"
              >
                <q-tooltip>Refresh list</q-tooltip>
              </q-btn>
              <q-btn
                color="primary"
                label="Upload New Form"
                icon="upload_file"
                :to="{name: 'form-ocr.upload'}"
              />
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading && forms.length === 0" class="text-center q-pa-xl">
            <q-spinner color="primary" size="3em" />
            <div class="q-mt-md text-grey-6">Loading forms...</div>
          </div>

          <!-- Empty State -->
          <div v-else-if="forms.length === 0" class="text-center q-pa-xl">
            <q-icon name="scanner" size="5em" color="grey-5" />
            <div class="text-h6 text-grey-6 q-mt-md">No forms processed yet</div>
            <div class="text-body2 text-grey-5 q-mb-md">
              Upload your first form to get started with OCR processing
            </div>
            <q-btn
              color="primary"
              label="Upload Form"
              icon="upload_file"
              :to="{name: 'form-ocr.upload'}"
            />
          </div>

          <!-- Form List -->
          <div v-else class="q-gutter-md">
            <q-card
              v-for="form in forms"
              :key="form.form_id"
              class="form-card"
              :class="{ 'form-card-expanded': expandedForm === form.form_id }"
            >
              <q-card-section>
                <div class="row items-start justify-between">
                  <div class="col">
                    <div class="text-h6 text-primary">{{ form.filename }}</div>
                    <div class="text-caption text-grey-6 q-mt-xs">
                      <q-icon name="event" size="xs" class="q-mr-xs" />
                      Uploaded: {{ formatDate(form.upload_date) }}
                    </div>
                    <div class="q-mt-sm q-gutter-xs">
                      <q-chip
                        :color="getStatusColor(form.processing_status)"
                        text-color="white"
                        size="sm"
                        :icon="getStatusIcon(form.processing_status)"
                      >
                        {{ form.processing_status }}
                      </q-chip>
                      <q-chip
                        color="info"
                        text-color="white"
                        size="sm"
                        icon="description"
                      >
                        {{ form.page_count }} {{ form.page_count === 1 ? 'page' : 'pages' }}
                      </q-chip>
                    </div>
                  </div>
                  <div class="col-auto q-gutter-xs">
                    <q-btn
                      flat
                      round
                      color="primary"
                      :icon="expandedForm === form.form_id ? 'expand_less' : 'expand_more'"
                      @click="toggleExpand(form.form_id)"
                      :loading="loadingDetails === form.form_id"
                    >
                      <q-tooltip>{{ expandedForm === form.form_id ? 'Collapse' : 'View details' }}</q-tooltip>
                    </q-btn>
                    <q-btn
                      flat
                      round
                      color="info"
                      icon="image"
                      @click="viewImages(form.form_id)"
                      :loading="loadingImages === form.form_id"
                    >
                      <q-tooltip>View images</q-tooltip>
                    </q-btn>
                    <q-btn
                      flat
                      round
                      color="negative"
                      icon="delete"
                      @click="deleteForm(form.form_id)"
                      :loading="deleting === form.form_id"
                    >
                      <q-tooltip>Delete form</q-tooltip>
                    </q-btn>
                  </div>
                </div>
              </q-card-section>

              <!-- Expanded Details -->
              <q-slide-transition>
                <div v-if="expandedForm === form.form_id && formDetails">
                  <q-separator />
                  <q-card-section>
                    <!-- Processing Info -->
                    <div class="q-mb-md">
                      <div class="text-subtitle1 text-weight-bold q-mb-sm">
                        <q-icon name="info" color="primary" />
                        Processing Information
                      </div>
                      <div class="q-pl-md q-gutter-xs">
                        <div><strong>Status:</strong> {{ formDetails.processing_status }}</div>
                        <div v-if="formDetails.results">
                          <strong>Processing Time:</strong> {{ formDetails.results.processing_time }}s
                        </div>
                        <div v-if="formDetails.results?.metadata">
                          <strong>OCR Engine:</strong> {{ formDetails.results.metadata.ocr_engine }}
                        </div>
                        <div v-if="formDetails.results?.metadata">
                          <strong>Language:</strong> {{ formDetails.results.metadata.language }}
                        </div>
                        <div v-if="formDetails.results?.metadata">
                          <strong>Segment Detection:</strong>
                          {{ formDetails.results.metadata.segment_detection_enabled ? 'Enabled' : 'Disabled' }}
                        </div>
                      </div>
                    </div>

                    <!-- Pages Summary -->
                    <div v-if="formDetails.results?.pages" class="q-mb-md">
                      <div class="text-subtitle1 text-weight-bold q-mb-sm">
                        <q-icon name="description" color="primary" />
                        Pages ({{ formDetails.results.pages.length }})
                      </div>
                      <div class="q-pl-md">
                        <q-list dense separator>
                          <q-item v-for="page in formDetails.results.pages" :key="page.page_number">
                            <q-item-section>
                              <q-item-label class="text-weight-bold">
                                Page {{ page.page_number }}
                              </q-item-label>
                              <q-item-label caption>
                                {{ page.text_regions.length }} text regions detected
                              </q-item-label>
                              <q-item-label caption>
                                {{ page.form_fields.length }} form fields extracted
                              </q-item-label>
                            </q-item-section>
                            <q-item-section side>
                              <q-chip
                                v-if="page.correction_applied"
                                color="positive"
                                text-color="white"
                                size="sm"
                                icon="check"
                              >
                                Corrected
                              </q-chip>
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                    </div>

                    <!-- Form Fields Summary -->
                    <div v-if="getAllFormFields(formDetails).length > 0" class="q-mb-md">
                      <div class="text-subtitle1 text-weight-bold q-mb-sm">
                        <q-icon name="list_alt" color="primary" />
                        All Form Fields ({{ getAllFormFields(formDetails).length }})
                      </div>
                      <div class="q-pl-md">
                        <q-list dense separator>
                          <q-item v-for="(field, index) in getAllFormFields(formDetails)" :key="index">
                            <q-item-section>
                              <q-item-label class="text-weight-bold">{{ field.label }}</q-item-label>
                              <q-item-label caption>
                                Value: {{ field.value || '(empty)' }}
                              </q-item-label>
                              <q-item-label caption>
                                Layout: {{ field.layout }}
                              </q-item-label>
                            </q-item-section>
                            <q-item-section side>
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
                    </div>

                    <!-- Form ID -->
                    <div class="q-mt-md q-pt-md" style="border-top: 1px solid #e0e0e0">
                      <div class="text-caption text-grey-6">
                        Form ID: {{ form.form_id }}
                      </div>
                    </div>
                  </q-card-section>
                </div>
              </q-slide-transition>
            </q-card>
          </div>
        </div>
      </div>
    </div>

    <!-- Images Dialog -->
    <q-dialog v-model="showImagesDialog" maximized>
      <q-card v-if="formImages">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Form Images</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-tabs
            v-model="selectedImagePage"
            dense
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            align="left"
          >
            <q-tab
              v-for="image in formImages.images"
              :key="image.page_number"
              :name="image.page_number"
              :label="`Page ${image.page_number}`"
            />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="selectedImagePage" animated>
            <q-tab-panel
              v-for="image in formImages.images"
              :key="image.page_number"
              :name="image.page_number"
            >
              <div class="row q-col-gutter-md">
                <div class="col-12 col-md-6">
                  <div class="text-subtitle2 q-mb-sm">Original Image</div>
                  <q-img
                    :src="`data:image/png;base64,${image.original}`"
                    class="rounded-borders"
                    fit="contain"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <div class="text-subtitle2 q-mb-sm">Corrected Image</div>
                  <q-img
                    :src="`data:image/png;base64,${image.corrected}`"
                    class="rounded-borders"
                    fit="contain"
                  />
                </div>
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </q-card-section>
      </q-card>
    </q-dialog>
  </a-section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// API base URL
const API_BASE_URL = 'http://localhost:8000'

// Types
interface FormListItem {
  form_id: string
  filename: string
  upload_date: string
  page_count: number
  processing_status: string
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
  text_regions: any[]
  form_fields: FormField[]
}

interface FormProcessResponse {
  form_id: string
  page_count: number
  processing_time: number
  pages: PageResult[]
  metadata: Record<string, any>
}

interface FormDetail {
  form_id: string
  filename: string
  upload_date: string
  page_count: number
  processing_status: string
  results: FormProcessResponse | null
}

interface FormImage {
  page_number: number
  original: string
  corrected: string
}

interface FormImagesResponse {
  form_id: string
  images: FormImage[]
}

// Reactive data
const forms = ref<FormListItem[]>([])
const loading = ref(false)
const deleting = ref<string | null>(null)
const expandedForm = ref<string | null>(null)
const formDetails = ref<FormDetail | null>(null)
const loadingDetails = ref<string | null>(null)
const showImagesDialog = ref(false)
const formImages = ref<FormImagesResponse | null>(null)
const loadingImages = ref<string | null>(null)
const selectedImagePage = ref(1)

// Load forms list
const loadForms = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/form-ocr/forms`)
    if (response.ok) {
      const data = await response.json()
      forms.value = data.forms
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('Error loading forms:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load forms',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    loading.value = false
  }
}

// Toggle expand form details
const toggleExpand = async (formId: string) => {
  if (expandedForm.value === formId) {
    expandedForm.value = null
    formDetails.value = null
  } else {
    expandedForm.value = formId
    await loadFormDetails(formId)
  }
}

// Load form details
const loadFormDetails = async (formId: string) => {
  loadingDetails.value = formId
  try {
    const response = await fetch(`${API_BASE_URL}/form-ocr/form/${formId}`)
    if (response.ok) {
      const data = await response.json()
      formDetails.value = data
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('Error loading form details:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load form details',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
    expandedForm.value = null
  } finally {
    loadingDetails.value = null
  }
}

// View images
const viewImages = async (formId: string) => {
  loadingImages.value = formId
  try {
    const response = await fetch(`${API_BASE_URL}/form-ocr/form/${formId}/images`)
    if (response.ok) {
      const data = await response.json()
      formImages.value = data
      selectedImagePage.value = data.images[0]?.page_number || 1
      showImagesDialog.value = true
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('Error loading form images:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load form images',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    loadingImages.value = null
  }
}

// Delete form
const deleteForm = async (formId: string) => {
  $q.dialog({
    title: 'Confirm Delete',
    message: 'Are you sure you want to delete this form? This action cannot be undone.',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    deleting.value = formId
    try {
      const response = await fetch(`${API_BASE_URL}/form-ocr/form/${formId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        $q.notify({
          type: 'positive',
          message: 'Form deleted successfully'
        })

        // Collapse if this form was expanded
        if (expandedForm.value === formId) {
          expandedForm.value = null
          formDetails.value = null
        }

        // Refresh the list
        await loadForms()
      } else {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }
    } catch (error) {
      console.error('Error deleting form:', error)
      $q.notify({
        type: 'negative',
        message: 'Failed to delete form',
        caption: error instanceof Error ? error.message : 'Unknown error'
      })
    } finally {
      deleting.value = null
    }
  })
}

// Get all form fields from all pages
const getAllFormFields = (formDetail: FormDetail): FormField[] => {
  if (!formDetail.results?.pages) return []

  const allFields: FormField[] = []
  formDetail.results.pages.forEach(page => {
    allFields.push(...page.form_fields)
  })
  return allFields
}

// Format date
const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr
  }
}

// Get status color
const getStatusColor = (status: string): string => {
  const colors: Record<string, string> = {
    completed: 'positive',
    processing: 'warning',
    failed: 'negative',
    pending: 'grey'
  }
  return colors[status] || 'grey'
}

// Get status icon
const getStatusIcon = (status: string): string => {
  const icons: Record<string, string> = {
    completed: 'check_circle',
    processing: 'pending',
    failed: 'error',
    pending: 'schedule'
  }
  return icons[status] || 'help'
}

// Get confidence color
const getConfidenceColor = (confidence: number): string => {
  if (confidence >= 0.8) return 'positive'
  if (confidence >= 0.6) return 'warning'
  return 'negative'
}

// Load forms on mount
onMounted(() => {
  loadForms()
})
</script>

<style scoped>
.form-card {
  transition: all 0.3s ease;
}

.form-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.form-card-expanded {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.rounded-borders {
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}
</style>
