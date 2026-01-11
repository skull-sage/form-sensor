<template>
  <a-section>
    <div class="q-pa-md">
      <div class="row justify-center">
        <div class="col-12 col-lg-10">
          <!-- Header -->
          <div class="row items-center justify-between q-mb-md">
            <div class="text-h5">
              <q-icon name="folder" class="q-mr-sm" />
              CV Library
            </div>
            <div class="q-gutter-sm">
              <q-btn
                flat
                round
                color="primary"
                icon="refresh"
                @click="loadCvs"
                :loading="loading"
              >
                <q-tooltip>Refresh list</q-tooltip>
              </q-btn>
              <q-btn
                color="primary"
                label="Upload New CV"
                icon="upload_file"
                :to="{name: 'doc-sensor.upload'}"
              />
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading && cvs.length === 0" class="text-center q-pa-xl">
            <q-spinner color="primary" size="3em" />
            <div class="q-mt-md text-grey-6">Loading CVs...</div>
          </div>

          <!-- Empty State -->
          <div v-else-if="cvs.length === 0" class="text-center q-pa-xl">
            <q-icon name="description" size="5em" color="grey-5" />
            <div class="text-h6 text-grey-6 q-mt-md">No CVs uploaded yet</div>
            <div class="text-body2 text-grey-5 q-mb-md">
              Upload your first CV to get started with analysis
            </div>
            <q-btn
              color="primary"
              label="Upload CV"
              icon="upload_file"
              :to="{name: 'doc-sensor.upload'}"
            />
          </div>

          <!-- CV List -->
          <div v-else class="q-gutter-md">
            <q-card
              v-for="cv in cvs"
              :key="cv.cv_id"
              class="cv-card"
              :class="{ 'cv-card-expanded': expandedCv === cv.cv_id }"
            >
              <q-card-section>
                <div class="row items-start justify-between">
                  <div class="col">
                    <div class="text-h6 text-primary">{{ cv.filename }}</div>
                    <div class="text-caption text-grey-6 q-mt-xs">
                      <q-icon name="event" size="xs" class="q-mr-xs" />
                      Uploaded: {{ formatDate(cv.upload_date) }}
                    </div>
                    <div class="q-mt-sm">
                      <q-chip
                        :color="cv.analyzed ? 'positive' : 'grey'"
                        text-color="white"
                        size="sm"
                        :icon="cv.analyzed ? 'check_circle' : 'pending'"
                      >
                        {{ cv.analyzed ? 'Analyzed' : 'Not Analyzed' }}
                      </q-chip>
                    </div>
                  </div>
                  <div class="col-auto q-gutter-xs">
                    <q-btn
                      flat
                      round
                      color="primary"
                      :icon="expandedCv === cv.cv_id ? 'expand_less' : 'expand_more'"
                      @click="toggleExpand(cv.cv_id)"
                      :loading="loadingDetails === cv.cv_id"
                    >
                      <q-tooltip>{{ expandedCv === cv.cv_id ? 'Collapse' : 'View details' }}</q-tooltip>
                    </q-btn>
                    <q-btn
                      flat
                      round
                      color="negative"
                      icon="delete"
                      @click="deleteCv(cv.cv_id)"
                      :loading="deleting === cv.cv_id"
                    >
                      <q-tooltip>Delete CV</q-tooltip>
                    </q-btn>
                  </div>
                </div>
              </q-card-section>

              <!-- Expanded Details -->
              <q-slide-transition>
                <div v-if="expandedCv === cv.cv_id && cvDetails">
                  <q-separator />
                  <q-card-section>
                    <!-- Basic Info -->
                    <div v-if="cvDetails.analysis?.basic_info" class="q-mb-md">
                      <div class="text-subtitle1 text-weight-bold q-mb-sm">
                        <q-icon name="person" color="primary" />
                        Basic Information
                      </div>
                      <div class="q-pl-md q-gutter-xs">
                        <div v-if="cvDetails.analysis.basic_info.name">
                          <strong>Name:</strong> {{ cvDetails.analysis.basic_info.name }}
                        </div>
                        <div v-if="cvDetails.analysis.basic_info.email">
                          <strong>Email:</strong> {{ cvDetails.analysis.basic_info.email }}
                        </div>
                        <div v-if="cvDetails.analysis.basic_info.phone">
                          <strong>Phone:</strong> {{ cvDetails.analysis.basic_info.phone }}
                        </div>
                        <div v-if="cvDetails.analysis.basic_info.address">
                          <strong>Location:</strong> {{ cvDetails.analysis.basic_info.address }}
                        </div>
                      </div>
                    </div>

                    <!-- Work Experience -->
                    <div v-if="cvDetails.analysis?.work_experience && cvDetails.analysis.work_experience.length > 0" class="q-mb-md">
                      <div class="text-subtitle1 text-weight-bold q-mb-sm">
                        <q-icon name="work" color="primary" />
                        Work Experience ({{ cvDetails.analysis.work_experience.length }})
                      </div>
                      <div class="q-pl-md">
                        <q-list dense separator>
                          <q-item v-for="(exp, index) in cvDetails.analysis.work_experience" :key="index">
                            <q-item-section>
                              <q-item-label class="text-weight-bold">{{ exp.company }}</q-item-label>
                              <q-item-label caption>
                                {{ formatDateRange(exp.start_date, exp.end_date) }}
                              </q-item-label>
                              <q-item-label caption class="text-grey-8 q-mt-xs">
                                {{ truncateText(exp.description, 150) }}
                              </q-item-label>
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                    </div>

                    <!-- Skills -->
                    <div v-if="cvDetails.analysis?.skill_keywords && cvDetails.analysis.skill_keywords.length > 0" class="q-mb-md">
                      <div class="text-subtitle1 text-weight-bold q-mb-sm">
                        <q-icon name="psychology" color="primary" />
                        Skills ({{ cvDetails.analysis.skill_keywords.length }})
                      </div>
                      <div class="q-pl-md q-gutter-xs">
                        <q-chip
                          v-for="skill in cvDetails.analysis.skill_keywords"
                          :key="skill"
                          color="teal"
                          text-color="white"
                          size="sm"
                        >
                          {{ skill }}
                        </q-chip>
                      </div>
                    </div>

                    <!-- Education -->
                    <div v-if="cvDetails.analysis?.education && cvDetails.analysis.education.length > 0">
                      <div class="text-subtitle1 text-weight-bold q-mb-sm">
                        <q-icon name="school" color="primary" />
                        Education ({{ cvDetails.analysis.education.length }})
                      </div>
                      <div class="q-pl-md">
                        <q-list dense separator>
                          <q-item v-for="(edu, index) in cvDetails.analysis.education" :key="index">
                            <q-item-section>
                              <q-item-label class="text-weight-bold">{{ edu.degree }}</q-item-label>
                              <q-item-label caption>{{ edu.institution }}</q-item-label>
                              <q-item-label caption v-if="edu.graduation_date">
                                {{ edu.graduation_date }}
                              </q-item-label>
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                    </div>

                    <!-- CV ID -->
                    <div class="q-mt-md q-pt-md" style="border-top: 1px solid #e0e0e0">
                      <div class="text-caption text-grey-6">
                        CV ID: {{ cv.cv_id }}
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
  </a-section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// API base URL
const API_BASE_URL = 'http://localhost:8000'

// Types
interface CVListItem {
  cv_id: string
  filename: string
  upload_date: string
  analyzed: boolean
}

interface BasicInfo {
  name: string | null
  email: string | null
  phone: string | null
  address: string | null
  social_links: Record<string, string>
}

interface WorkExperience {
  company: string
  start_date: string | null
  end_date: string | null
  description: string
}

interface Education {
  degree: string
  institution: string
  graduation_date: string | null
}

interface CVAnalysis {
  cv_id: string
  basic_info: BasicInfo
  work_experience: WorkExperience[]
  skill_keywords: string[]
  education: Education[]
}

interface CVDetail {
  id: string
  filename: string
  upload_date: string
  pages: number
  raw_text: string
  file_size: number
  analysis: CVAnalysis | null
}

// Reactive data
const cvs = ref<CVListItem[]>([])
const loading = ref(false)
const deleting = ref<string | null>(null)
const expandedCv = ref<string | null>(null)
const cvDetails = ref<CVDetail | null>(null)
const loadingDetails = ref<string | null>(null)

// Load CVs list
const loadCvs = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/doc-sensor/cvs`)
    if (response.ok) {
      const data = await response.json()
      cvs.value = data.cvs
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('Error loading CVs:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load CVs',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    loading.value = false
  }
}

// Toggle expand CV details
const toggleExpand = async (cvId: string) => {
  if (expandedCv.value === cvId) {
    expandedCv.value = null
    cvDetails.value = null
  } else {
    expandedCv.value = cvId
    await loadCvDetails(cvId)
  }
}

// Load CV details
const loadCvDetails = async (cvId: string) => {
  loadingDetails.value = cvId
  try {
    const response = await fetch(`${API_BASE_URL}/doc-sensor/cv/${cvId}`)
    if (response.ok) {
      const data = await response.json()
      cvDetails.value = data
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('Error loading CV details:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load CV details',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
    expandedCv.value = null
  } finally {
    loadingDetails.value = null
  }
}

// Delete CV
const deleteCv = async (cvId: string) => {
  $q.dialog({
    title: 'Confirm Delete',
    message: 'Are you sure you want to delete this CV? This action cannot be undone.',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    deleting.value = cvId
    try {
      const response = await fetch(`${API_BASE_URL}/doc-sensor/cv/${cvId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        $q.notify({
          type: 'positive',
          message: 'CV deleted successfully'
        })

        // Collapse if this CV was expanded
        if (expandedCv.value === cvId) {
          expandedCv.value = null
          cvDetails.value = null
        }

        // Refresh the list
        await loadCvs()
      } else {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }
    } catch (error) {
      console.error('Error deleting CV:', error)
      $q.notify({
        type: 'negative',
        message: 'Failed to delete CV',
        caption: error instanceof Error ? error.message : 'Unknown error'
      })
    } finally {
      deleting.value = null
    }
  })
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

// Format date range
const formatDateRange = (startDate: string | null, endDate: string | null): string => {
  if (!startDate && !endDate) return 'Date not specified'
  if (!startDate) return `Until ${endDate}`
  if (!endDate) return `From ${startDate}`
  return `${startDate} - ${endDate}`
}

// Truncate text
const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// Load CVs on mount
onMounted(() => {
  loadCvs()
})
</script>

<style scoped>
.cv-card {
  transition: all 0.3s ease;
}

.cv-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.cv-card-expanded {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>
