<template>
  <q-layout view="lHh Lpr lFf" class=" background">
    <q-header elevated  class="bg-dark">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Mando Store
        </q-toolbar-title>

        <div>lucal's films</div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>

</script>

<style>
.background{
  background-image: url("../assets/3rs2yx311cu31.webp");
  background-size:cover ;
}
</style>
