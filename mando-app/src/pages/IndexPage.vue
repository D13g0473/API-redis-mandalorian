<template>
  <q-page class="q-pa-md" >

      <q-table
        :rows="chapters"
        :columns="columns"
        row-key="id"
        flat
        bordered
        class="my-table"
        elevated
      >
      <template v-slot:top>
        <div class="row col-12">
          <div class="col-11">
            <center>
              <h5>{{ title }}</h5>
            </center>    
          </div>
          <q-space></q-space>
          <div class="col-1">
            <q-btn
                icon="refresh"
                @click="fetchChapters()"
                />
          </div>   
        </div>
  
      </template>
        <template v-slot:body-cell-status="props" >
          <q-td  align="center" class="q-gutter-xs" style="width: 120px;">
            <q-chip
             square
            :color="getStatusColor(props.row.status)"
            class="text-white"
          >
            {{ props.row.status }}
          </q-chip>
          </q-td>

        </template>
        

        <template v-slot:body-cell-actions="props">
          <q-td  align="center" class="q-gutter-xs" style="width: 120px;" >
            <q-btn
            v-if="props.row.status === 'available'"
            color="primary"
            @click="reserveChapter(props.row.id)"
          >
            Reservar
          </q-btn>
          <q-btn
            v-if="props.row.status === 'reserved'"
            color="green"
            @click="confirmChapter(props.row.id)"
          >
            Confirmar
          </q-btn>
          </q-td>
        </template>
      </q-table>
    <!-- </q-card> -->
  </q-page>
</template>

<script>
import axios from "axios";
import { useQuasar} from 'quasar'
import { ref } from "vue";

export default {
  data() {
    return {
      title:"Capítulos de The Mandalorian",
      chapters: ref([]), // Datos de los capítulos
      url: " http://localhost:5000/",
      $q : useQuasar(), 
      columns: [
      { name: "id", label: "ID", align: "left", field: "id" },
      { name: "title", label: "Título", align: "left", field: "title" },
      { name: "status", label: "Estado", align: "center", field: "status" },
      { name: "actions", label: "Acciones", align: "left", field: "actions" },
      ],
    };
  },
  methods: {
    async fetchChapters() {
      try {
        const response = await axios.get(this.url+"chapters");
        console.log(response);
        this.chapters = response.data;
      } catch (error) {
        console.error("Error fetching chapters:", error);
      }
    },
    async reserveChapter(chapterId) {
      try {
        const response = await axios.post(
          `${this.url}rent/${chapterId}`
        );
        this.$q.notify({ type: "positive", message: response.data.message });
        await this.fetchChapters(); // Actualiza la lista de capítulos
      } catch (error) {
        this.$q.notify({ type: "negative", message: error.response.data.error });
      }
    },
    async confirmChapter(chapterId) {
      try {
        const response = await axios.post(
          `${this.url}confirm/${chapterId}`,
          { price: 4.99 }
        );
        this.$q.notify({ type: "positive", message: response.data.message });
       await this.fetchChapters(); // Actualiza la lista de capítulos
      } catch (error) {
        this.$q.notify({ type: "negative", message: error.response.data.error });
      }
    },
    getStatusColor(status) {
      switch (status) {
        case "available":
          return "green";
        case "reserved":
          return "orange";
        case "rented":
          return "red";
        default:
          return "grey";
      }
    },
  },
  mounted() {
    this.fetchChapters();
  },
};
</script>

<style>
.my-table {
  max-width: 800px;
  margin: auto;
  background-color: rgba(116, 132, 143, 0.918);
}
.transparent{
  background-color: rgba(58, 57, 57, 0);
}
</style>
