<template>
  <a-section>
    <div class="q-pa-md">
      <div class="row justify-center">
        <div class="col-12 col-md-10 col-lg-8">
          <!-- Upload Card -->
          <q-card class="q-mb-lg" v-if="!analysisResult">
            <q-card-section>
              <div class="text-h5 q-mb-md">
                <q-icon name="upload_file" class="q-mr-sm" />
                Upload CV for Analysis
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
                  (val: File | null) => (val && val.size <= 10485760) || 'File size must be less than 10MB'
                ]"
                @update:model-value="onFileSelected"
              >
                <template v-slot:prepend>
                  <q-icon name="attach_file" />
                </template>
                <template v-slot:hint>
                  Upload a CV in PDF format (max 10MB)
                </template>
              </q-file>

              <div class="q-mt-md row justify-end">
                <q-btn
                  color="primary"
                  label="Analyze CV"
                  icon="analytics"
                  :loading="analyzing"
                  :disable="!selectedFile"
                  @click="analyzeCv"
                />
              </div>
            </q-card-section>
          </q-card>

          <!-- Analysis Result -->
          <div v-if="analysisResult">
            <q-card class="q-mb-md">
              <q-card-section class="bg-primary text-white">
                <div class="row items-center justify-between">
                  <div class="text-h6">
                    <q-icon name="check_circle" class="q-mr-sm" />
                    CV Analysis Complete
                  </div>
                  <q-btn
                    flat
                    round
                    icon="close"
                    @click="resetAnalysis"
                  >
                    <q-tooltip>Upload another CV</q-tooltip>
                  </q-btn>
                </div>
                <div class="text-caption">CV ID: {{ analysisResult.cv_id }}</div>
              </q-card-section>
            </q-card>

            <!-- Basic Info -->
            <q-card class="q-mb-md" v-if="analysisResult.basic_info">
              <q-card-section>
                <div class="text-h6 q-mb-md">
                  <q-icon name="person" color="primary" class="q-mr-sm" />
                  Basic Information
                </div>

                <div class="q-gutter-sm">
                  <div v-if="analysisResult.basic_info.name" class="row">
                    <div class="col-3 text-weight-bold">Name:</div>
                    <div class="col">{{ analysisResult.basic_info.name }}</div>
                  </div>
                  <div v-if="analysisResult.basic_info.email" class="row">
                    <div class="col-3 text-weight-bold">Email:</div>
                    <div class="col">
                      <a :href="`mailto:${analysisResult.basic_info.email}`">
                        {{ analysisResult.basic_info.email }}
                      </a>
                    </div>
                  </div>
                  <div v-if="analysisResult.basic_info.phone" class="row">
                    <div class="col-3 text-weight-bold">Phone:</div>
                    <div class="col">{{ analysisResult.basic_info.phone }}</div>
                  </div>
                  <div v-if="analysisResult.basic_info.address" class="row">
                    <div class="col-3 text-weight-bold">Location:</div>
                    <div class="col">{{ analysisResult.basic_info.address }}</div>
                  </div>
                  <div v-if="analysisResult.basic_info.social_links && Object.keys(analysisResult.basic_info.social_links).length > 0" class="row">
                    <div class="col-3 text-weight-bold">Links:</div>
                    <div class="col">
                      <div class="q-gutter-xs">
                        <q-chip
                          v-for="(url, platform) in analysisResult.basic_info.social_links"
                          :key="platform"
                          clickable
                          :icon="getSocialIcon(platform)"
                          color="primary"
                          text-color="white"
                          size="sm"
                          @click="openLink(url)"
                        >
                          {{ platform }}
                        </q-chip>
                      </div>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>

            <!-- Work Experience -->
            <q-card class="q-mb-md" v-if="analysisResult.work_experience && analysisResult.work_experience.length > 0">
              <q-card-section>
                <div class="text-h6 q-mb-md">
                  <q-icon name="work" color="primary" class="q-mr-sm" />
                  Work Experience
                </div>

                <q-timeline color="primary">
                  <q-timeline-entry
                    v-for="(exp, index) in analysisResult.work_experience"
                    :key="index"
                    :subtitle="formatDateRange(exp.start_date, exp.end_date)"
                  >
                    <template v-slot:title>
                      <div class="text-weight-bold">{{ exp.company }}</div>
                    </template>
                    <div class="text-body2">{{ exp.description }}</div>
                  </q-timeline-entry>
                </q-timeline>
              </q-card-section>
            </q-card>

            <!-- Skills -->
            <q-card class="q-mb-md" v-if="analysisResult.skill_keywords && analysisResult.skill_keywords.length > 0">
              <q-card-section>
                <div class="text-h6 q-mb-md">
                  <q-icon name="psychology" color="primary" class="q-mr-sm" />
                  Skills & Keywords
                </div>

                <div class="q-gutter-xs">
                  <q-chip
                    v-for="skill in analysisResult.skill_keywords"
                    :key="skill"
                    color="teal"
                    text-color="white"
                    size="md"
                  >
                    {{ skill }}
                  </q-chip>
                </div>
              </q-card-section>
            </q-card>

            <!-- Education -->
            <q-card class="q-mb-md" v-if="analysisResult.education && analysisResult.education.length > 0">
              <q-card-section>
                <div class="text-h6 q-mb-md">
                  <q-icon name="school" color="primary" class="q-mr-sm" />
                  Education
                </div>

                <q-list separator>
                  <q-item v-for="(edu, index) in analysisResult.education" :key="index">
                    <q-item-section>
                      <q-item-label class="text-weight-bold">{{ edu.degree }}</q-item-label>
                      <q-item-label caption>{{ edu.institution }}</q-item-label>
                      <q-item-label caption v-if="edu.graduation_date">
                        Graduated: {{ edu.graduation_date }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-card-section>
            </q-card>

            <!-- Actions -->
            <div class="row q-gutter-sm justify-center q-mt-md">
              <q-btn
                color="primary"
                label="Upload Another CV"
                icon="upload_file"
                @click="resetAnalysis"
              />
              <q-btn
                color="secondary"
                label="View All CVs"
                icon="list"
                :to="{name: 'doc-sensor.list'}"
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

interface CVAnalysisResponse {
  cv_id: string
  basic_info: BasicInfo
  work_experience: WorkExperience[]
  skill_keywords: string[]
  education: Education[]
}

// Reactive data
const selectedFile = ref<File | null>(null)
const analyzing = ref(false)
const analysisResult = ref<CVAnalysisResponse | null>(null)

// File selection handler
const onFileSelected = (file: File | null) => {
  if (file) {
    console.log('File selected:', file.name, file.size, 'bytes')
  }
}

// Analyze CV
const analyzeCv = async () => {
  if (!selectedFile.value) {
    $q.notify({
      type: 'negative',
      message: 'Please select a PDF file'
    })
    return
  }

  analyzing.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await fetch(`${API_BASE_URL}/doc-sensor/analyze-cv`, {
      method: 'POST',
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      analysisResult.value = data

      $q.notify({
        type: 'positive',
        message: 'CV analyzed successfully',
        caption: `CV ID: ${data.cv_id}`
      })
    } else {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }
  } catch (error) {
    console.error('Error analyzing CV:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to analyze CV',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    analyzing.value = false
  }
}

// Reset analysis
const resetAnalysis = () => {
  selectedFile.value = null
  analysisResult.value = null
}

// Format date range
const formatDateRange = (startDate: string | null, endDate: string | null): string => {
  if (!startDate && !endDate) return 'Date not specified'
  if (!startDate) return `Until ${endDate}`
  if (!endDate) return `From ${startDate}`
  return `${startDate} - ${endDate}`
}

// Get social icon
const getSocialIcon = (platform: string): string => {
  const icons: Record<string, string> = {
    linkedin: 'fab fa-linkedin',
    github: 'fab fa-github',
    portfolio: 'language',
    twitter: 'fab fa-twitter'
  }
  return icons[platform.toLowerCase()] || 'link'
}

// Open link
const openLink = (url: string) => {
  window.open(url, '_blank')
}
</script>

<style scoped>
.q-timeline {
  padding-left: 0;
}
</style>
