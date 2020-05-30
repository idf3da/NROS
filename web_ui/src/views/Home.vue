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
							<yandex-map :zoom="13" :coords="[55.753, 37.62]" :controls="[]" style="height: 300px;" @map-was-initialized="initHandler">
								<ymap-marker marker-type="circle" :coords="[55.765, 37.6]" circle-radius="700" hint-content="Cool loot zone" marker-id="1" :marker-fill="{ color: '#00FFFF', opacity: 0.5 }" :balloon="{ header: 'Cool loot', body: 'Probability of high loot here is increased' }"></ymap-marker>
								<ymap-marker marker-type="circle" :coords="[55.75, 37.63]" circle-radius="1500" hint-content="Next zone" marker-id="2" :marker-fill="{ color: '#D8D8D8', opacity: 0.3 }" :balloon="{ header: 'Next zone' }" :marker-stroke="{ color: '#808080', width: 2, opacity: 1 }"></ymap-marker>
								<ymap-marker :coords="[55.745, 37.6]" marker-id="3" hint-content="That's you" :icon="markerIcon" />
								<ymap-marker :coords="[55.755, 37.59]" marker-id="4" hint-content="Store" :icon="storeIcon" />
								<ymap-marker :coords="[55.755, 37.63]" marker-id="5" hint-content="Store" :icon="storeIcon" />
								<ymap-marker :coords="[55.74, 37.62]" marker-id="6" hint-content="Store" :icon="storeIcon" />
								<ymap-marker :coords="[55.77, 37.62]" marker-id="7" hint-content="Warehouse" :icon="wareHouseIcon" />
							</yandex-map>
						</v-card-text>
					</v-card>
				</v-col>
				<v-responsive style="width: 100%"></v-responsive>
				<v-col>
					<v-card :loading="switch1" style="width: 100%" class="pa-0" outlined tile>
						<v-card-title class="mt-n9"
							>Optimization options

							<v-col class="ml-5 mt-1"
								><v-checkbox v-model="checkbox1" label="Магазин 1"></v-checkbox>
								<v-checkbox class="mt-n4" v-model="checkbox1" label="Магазин 2"></v-checkbox>
							</v-col>
							<v-switch class="mr-5" v-model="switch1" color="blue" label="Use seasonal algorithm"></v-switch>
							<v-btn color="success" :loading="switch1" large>Make <br />New suggestion</v-btn>
						</v-card-title>
						<v-data-table :headers="store_headers" :items="store_data" :expanded.sync="expanded" item-key="shopID" show-expand :search="table_search" :options.sync="table_pagination">
							<template v-slot:top>
								<v-toolbar flat>
									<v-toolbar-title>Your properties</v-toolbar-title>
								</v-toolbar>
							</template>
							<template v-slot:expanded-item="{}">
								<v-spacer></v-spacer>
								<td :colspan="2">
									<v-data-table hide-default-footer :headers="product_headers" :items="product_data" :items-per-page="1000" elevation-0>
										<template v-slot:top>
											<v-toolbar flat>
												<v-toolbar-title caption>Properties products</v-toolbar-title>
											</v-toolbar>
										</template>
									</v-data-table>
								</td>
								<v-spacer></v-spacer>
							</template>
						</v-data-table>
						<div class="text-xs-center pt-2">
							<v-options v-model="table_pagination.page" :length="pages"></v-options>
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
				expanded: [],
				module1: "",
				table_pagination: {},
				table_selected: [],
				store_headers: [
					{ text: "Name", value: "name" },
					{ text: "Address", value: "address" },
					{ text: "Longtitude", value: "longtitude" },
					{ text: "Latitude", value: "latitude" },
					{ text: "Fullness", value: "fullness" },
					{ text: "Capacity", value: "capacity" },
				],
				product_headers: [
					{ text: "Name", value: "name" },
					{ text: "price", value: "price" },
					{ text: "seasonDay", value: "seasonDay" },
				],
				store_data: [
					{
						name: "Магазин 1",
						address: "Тимура фрунзе, 4",
						longtitude: 0,
						latitude: 0,
						fullness: 30,
						capacity: 14,
						minRequired: 10,
						shop: false,
						shopID: 1,
					},
					{
						name: "Магазин 2",
						address: "Проспект мира, 8б",
						longtitude: 0,
						latitude: 0,
						fullness: 80,
						capacity: 27,
						minRequired: 15,
						shop: true,
						shopID: 2,
					},
				],
				product_data: [
					{
						name: "Bread",
						price: 60,
						seasonDay: 365,
					},
					{
						name: "Ice cream sandwich",
						price: 140,
						seasonDay: 365,
					},
					{
						name: "Eclair",
						price: 80,
						seasonDay: 365,
					},
					{
						name: "Cupcake",
						price: 70,
						seasonDay: 365,
					},
					{
						name: "Gingerbread",
						price: 40,
						seasonDay: 365,
					},
					{
						name: "Jelly bean",
						price: 110,
						seasonDay: 365,
					},
					{
						name: "Lollipop",
						price: 30,
						seasonDay: 365,
					},
					{
						name: "Honeycomb",
						price: 40,
						seasonDay: 365,
					},
					{
						name: "Donut",
						price: 45,
						seasonDay: 365,
					},
					{
						name: "KitKat",
						price: 65,
						seasonDay: 365,
					},
				],
			};
		},
		created() {
			axios.get("http://127.0.0.1:5000/api/locations").then((response) => {
				this.locations = response.data.locations;
			});
		},
	};
</script>
