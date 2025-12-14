<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <!-- Left Panel - Add Predefined Descriptions -->
      <div class="col-md-5 col-12">
        <q-card class="q-mb-md">
          <q-card-section>
            <div class="text-h6">Add Predefined Description</div>
          </q-card-section>
          <q-card-section>
            <q-form @submit="addDescription">
              <q-input
                v-model="newDescription.id"
                label="ID"
                outlined
                class="q-mb-md"
                :rules="[val => !!val || 'ID is required']"
              />
              <q-input
                v-model="newDescription.text"
                label="Description Text"
                type="textarea"
                outlined
                rows="3"
                class="q-mb-md"
                :rules="[val => !!val || 'Description is required']"
              />
              <q-input
                v-model="newDescription.category"
                label="Category"
                outlined
                class="q-mb-md"
              />
              <q-btn
                type="submit"
                color="primary"
                label="Add Description"
                :loading="loading"
              />
            </q-form>
          </q-card-section>
        </q-card>

        <!-- Predefined Descriptions List -->
        <q-card>
          <q-card-section>
            <div class="text-h6">Predefined Descriptions ({{ descriptions.length }})</div>
          </q-card-section>
          <q-card-section>
            <q-list separator>
              <q-item v-for="desc in descriptions" :key="desc.id">
                <q-item-section>
                  <q-item-label class="text-weight-bold">{{ desc.id }}</q-item-label>
                  <q-item-label caption>{{ desc.text }}</q-item-label>
                  <q-item-label caption class="text-blue">{{ desc.category }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-btn
                    flat
                    round
                    color="negative"
                    icon="delete"
                    @click="deleteDescription(desc.id)"
                  />
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <!-- Right Panel - Similarity Check -->
      <div class="col-md-6 col-12">
        <q-card class="q-mb-md">
          <q-card-section>
            <div class="text-h6">Semantic Similarity Check</div>
          </q-card-section>
          <q-card-section>
            <q-form @submit="checkSimilarity">
              <q-input
                v-model="similarityCheck.text"
                label="Text to Check"
                type="textarea"
                outlined
                rows="4"
                class="q-mb-md"
                :rules="[val => !!val || 'Text is required']"
              />
              <q-slider
                v-model="similarityCheck.threshold"
                :min="0"
                :max="1"
                :step="0.05"
                label
                :label-value="`Threshold: ${similarityCheck.threshold}`"
                class="q-mb-md"
              />
              <q-btn
                type="submit"
                color="secondary"
                label="Check Similarity"
                :loading="checkingLoading"
                :disable="descriptions.length === 0"
              />
            </q-form>
          </q-card-section>
        </q-card>

        <!-- Results -->
        <q-card v-if="results">
          <q-card-section>
            <div class="text-h6">Results</div>
          </q-card-section>
          <q-card-section>
            <div v-if="results.best_match" class="q-mb-md">
              <div class="text-subtitle1 text-weight-bold text-green">Best Match:</div>
              <q-chip
                :label="`${results.best_match.id} (${(results.best_match.similarity * 100).toFixed(1)}%)`"
                color="green"
                text-color="white"
              />
              <div class="q-mt-sm">{{ results.best_match.text }}</div>
            </div>

            <div v-if="results.matches.length > 0">
              <div class="text-subtitle1 text-weight-bold">All Matches Above Threshold:</div>
              <q-list>
                <q-item v-for="match in results.matches" :key="match.id">
                  <q-item-section>
                    <q-item-label>{{ match.id }}</q-item-label>
                    <q-item-label caption>{{ match.text }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-chip
                      :label="`${(match.similarity * 100).toFixed(1)}%`"
                      :color="match.similarity > 0.8 ? 'green' : match.similarity > 0.6 ? 'orange' : 'red'"
                      text-color="white"
                    />
                  </q-item-section>
                </q-item>
              </q-list>
            </div>

            <div v-else class="text-negative">
              No matches found above the threshold of {{ (similarityCheck.threshold * 100).toFixed(0) }}%
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const API_BASE = 'http://localhost:8000'

const loading = ref(false)
const checkingLoading = ref(false)
const descriptions = ref([])
const results = ref(null)

const newDescription = ref({
  id: '',
  text: '',
  category: 'general'
})

const similarityCheck = ref({
  text: '',
  threshold: 0.7
})

const addDescription = async () => {
  loading.value = true
  try {
    await axios.post(`${API_BASE}/descriptions/add`, newDescription.value)
    $q.notify({
      type: 'positive',
      message: 'Description added successfully'
    })
    newDescription.value = { id: '', text: '', category: 'general' }
    await loadDescriptions()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to add description'
    })
  } finally {
    loading.value = false
  }
}

const loadDescriptions = async () => {
  try {
    const response = await axios.get(`${API_BASE}/descriptions`)
    descriptions.value = response.data.descriptions
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to load descriptions'
    })
  }
}

const deleteDescription = async (id: string) => {
  try {
    await axios.delete(`${API_BASE}/descriptions/${id}`)
    $q.notify({
      type: 'positive',
      message: 'Description deleted'
    })
    await loadDescriptions()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to delete description'
    })
  }
}

const checkSimilarity = async () => {
  checkingLoading.value = true
  try {
    const response = await axios.post(`${API_BASE}/similarity/check`, similarityCheck.value)
    results.value = response.data
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to check similarity'
    })
  } finally {
    checkingLoading.value = false
  }
}

onMounted(() => {
  loadDescriptions()
})
</script>
