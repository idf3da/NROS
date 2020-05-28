<template>
	<div class="home">
		<v-container fluid>
			<v-row align="start" justify="space-around">
				<v-col>
					<v-card class="pa-1" outlined tile :loading="switch1">
						<v-card-title>
							Product Items
							<v-spacer></v-spacer>
							<v-text-field v-model="search1" append-icon="mdi-magnify" label="Search" hide-details></v-text-field>
						</v-card-title>
						<v-data-table :height="185" :headers="headers1" :items="locations" :search="search1"></v-data-table>
					</v-card>
				</v-col>
				<v-col>
					<v-card outlined tile>
						<v-card-text class="px-0">
							<yandex-map :zoom="13" :coords="[55.753, 37.62]" :controls="[]" style="height: 300px;" :placemarks="placemarks" @map-was-initialized="initHandler">
								<ymap-marker marker-type="circle" :coords="[55.753, 37.62]" circle-radius="4500" hint-content="Zone" marker-id="0" :marker-fill="{ color: '#000', opacity: 0 }" :marker-stroke="{ color: '#ff0000', width: 200, opacity: 0.5 }" :balloon="{ header: 'Это зона', body: 'вы в зоне', footer: 'Урона нет' }"></ymap-marker>
								<ymap-marker marker-type="circle" :coords="[55.765, 37.6]" circle-radius="700" hint-content="Cool loot zone" marker-id="1" :marker-fill="{ color: '#00FFFF', opacity: 0.5 }" :balloon="{ header: 'Cool loot', body: 'Probability of high loot here is increased' }"></ymap-marker>
								<ymap-marker marker-type="circle" :coords="[55.75, 37.63]" circle-radius="1500" hint-content="Next zone" marker-id="2" :marker-fill="{ color: '#D8D8D8', opacity: 0.3 }" :balloon="{ header: 'Next zone' }" :marker-stroke="{ color: '#808080', width: 2, opacity: 1 }"></ymap-marker>
								<ymap-marker :coords="[55.745, 37.6]" marker-id="3" hint-content="That's you" :icon="markerIcon" />
								<ymap-marker :coords="[55.755, 37.59]" marker-id="4" hint-content="Store" :icon="storeIcon" />
								<ymap-marker :coords="[55.755, 37.63]" marker-id="5" hint-content="Store" :icon="storeIcon" />
								<ymap-marker :coords="[55.77, 37.62]" marker-id="6" hint-content="Warehouse" :icon="wareHouseIcon" />
							</yandex-map>
						</v-card-text>
					</v-card>
				</v-col>
				<v-responsive style="width: 100%"></v-responsive>
				<v-col>
					<v-card :loading="switch1" style="width: 100%" class="pa-0" outlined tile>
						<v-card-title
							>Optimization options
							<v-spacer />
							<v-checkbox v-model="checkbox1" label="Store 1"></v-checkbox>
							<v-spacer />
							<v-checkbox v-model="checkbox1" label="Store 2"></v-checkbox>
							<v-spacer />
							<v-switch v-model="switch1" color="blue" label="Use something"></v-switch>
							<v-spacer />
							<v-spacer></v-spacer>
							<v-text>
								<v-row>
									<v-btn color="success" :loading="switch1" large>Make <br />New suggestion</v-btn>
								</v-row>
							</v-text>
						</v-card-title>
						<v-data-table :headers="table_headers" :items="table_data" :search="table_search" hide-actions :pagination.sync="table_pagination" class="elevation-1">
							<template v-slot:items="props">
								<td>{{ props.item.name }}</td>
								<td class="text-xs-right">{{ props.item.calories }}</td>
								<td class="text-xs-right">{{ props.item.fat }}</td>
								<td class="text-xs-right">{{ props.item.carbs }}</td>
								<td class="text-xs-right">{{ props.item.protein }}</td>
								<td class="text-xs-right">{{ props.item.iron }}</td>
							</template>
						</v-data-table>
						<div class="text-xs-center pt-2">
							<v-pagination v-model="table_pagination.page" :length="pages"></v-pagination>
						</div>
					</v-card>
				</v-col>
			</v-row>
		</v-container>
	</div>
</template>
<script>
	import { yandexMap, ymapMarker } from "vue-yandex-maps";
	import axios from "axios";

	export default {
		name: "VueChartJS",
		components: {
			yandexMap,
			ymapMarker,
		},
		data() {
			return {
				markerIcon: {
					layout: "default#imageWithContent",
					imageHref: "https://cdn2.iconfinder.com/data/icons/maps-navigation-glyph-black/614/3719_-_Pointer_I-512.png",
					imageSize: [43, 43],
					imageOffset: [0, 0],
					contentOffset: [0, 15],
					contentLayout: '<div style="background: red; width: 50px; color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>',
				},
				storeIcon: {
					layout: "default#imageWithContent",
					imageHref: "https://image.flaticon.com/icons/png/512/1892/1892627.png",
					imageSize: [43, 43],
					imageOffset: [0, 0],
					contentOffset: [0, 15],
					contentLayout: '<div style="background: red; width: 50px; color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>',
				},
				wareHouseIcon: {
					layout: "default#imageWithContent",
					imageHref: "https://cdn4.iconfinder.com/data/icons/supermarket-32/512/warehouse-storage-stocks-store-512.png",
					imageSize: [43, 43],
					imageOffset: [0, 0],
					contentOffset: [0, 15],
					contentLayout: '<div style="background: red; width: 50px; color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>',
				},
				search1: "",
				table_search: "",
				switch1: false,
				module1: "",
				headers1: [
					{
						text: "Location Id",
						align: "start",
						value: "id",
					},
					{ text: "Address", value: "address" },
					{ text: "Latitude", value: "latitude" },
					{ text: "Longitude", value: "longitude" },
				],
				table_pagination: {},
				table_selected: [],
				table_headers: [
					{
						text: "Dessert (100g serving)",
						align: "left",
						sortable: false,
						value: "name",
					},
					{ text: "Calories", value: "calories" },
					{ text: "Fat (g)", value: "fat" },
					{ text: "Carbs (g)", value: "carbs" },
					{ text: "Protein (g)", value: "protein" },
					{ text: "Iron (%)", value: "iron" },
				],
				table_data: [
					{
						name: "Frozen Yogurt",
						calories: 159,
						fat: 6.0,
						carbs: 24,
						protein: 4.0,
						iron: "1%",
					},
					{
						name: "Ice cream sandwich",
						calories: 237,
						fat: 9.0,
						carbs: 37,
						protein: 4.3,
						iron: "1%",
					},
					{
						name: "Eclair",
						calories: 262,
						fat: 16.0,
						carbs: 23,
						protein: 6.0,
						iron: "7%",
					},
					{
						name: "Cupcake",
						calories: 305,
						fat: 3.7,
						carbs: 67,
						protein: 4.3,
						iron: "8%",
					},
					{
						name: "Gingerbread",
						calories: 356,
						fat: 16.0,
						carbs: 49,
						protein: 3.9,
						iron: "16%",
					},
					{
						name: "Jelly bean",
						calories: 375,
						fat: 0.0,
						carbs: 94,
						protein: 0.0,
						iron: "0%",
					},
					{
						name: "Lollipop",
						calories: 392,
						fat: 0.2,
						carbs: 98,
						protein: 0,
						iron: "2%",
					},
					{
						name: "Honeycomb",
						calories: 408,
						fat: 3.2,
						carbs: 87,
						protein: 6.5,
						iron: "45%",
					},
					{
						name: "Donut",
						calories: 452,
						fat: 25.0,
						carbs: 51,
						protein: 4.9,
						iron: "22%",
					},
					{
						name: "KitKat",
						calories: 518,
						fat: 26.0,
						carbs: 65,
						protein: 7,
						iron: "6%",
					},
				],
			};
		},
		mounted() {
			axios.get("http://127.0.0.1:5000/api/locations").then((response) => {
				this.locations = response.data.locations;
			});
		},
	};
</script>
