<template>
	<div class="home">
		<v-container fluid>
			{{ product_items }}
			<br />
			{{ property_items }}
			<br />
			{{ store_data[0].productArr }}
			<v-row align="start" justify="space-around">
				<v-col>
					<v-card class="pa-1" outlined tile :loading="switch1">
						<v-card-title>
							Product Items
							<v-spacer></v-spacer>
							<v-text-field v-model="search1" append-icon="mdi-magnify" label="Search" hide-details></v-text-field>
						</v-card-title>
						<v-data-table :height="185" :headers="product_items_headers" :items="product_items" :search="search1"></v-data-table>
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
						<v-data-table :headers="store_headers" :items="store_data" item-key="shopID" show-expand :search="table_search" :options.sync="table_pagination">
							<template v-slot:top>
								<v-toolbar flat>
									<v-toolbar-title>Your properties</v-toolbar-title>
								</v-toolbar>
							</template>

							<template v-slot:expanded-item="{ item }">
								<v-spacer></v-spacer>
								<td :colspan="2">
									<v-data-table hide-default-footer :height="300" :headers="property_product_headers" :items="item.productArr" :items-per-page="100" elevation-0>
										<template v-slot:top>
											<v-toolbar flat>
												<v-toolbar-title caption>{{ each_store_products }}</v-toolbar-title>
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
					{ text: "Store ID", value: "point_id" },
					{ text: "Address", value: "address" },
					{ text: "Longtitude", value: "longtitude" },
					{ text: "Latitude", value: "latitude" },
					{ text: "Fullness", value: "fullness" },
					{ text: "Capacity", value: "capacity" },
					{ text: "Minimum", value: "minimum" },
				],
				product_items_headers: [
					{ text: "Name", value: "name" },
					{ text: "Product ID", value: "product_type_id" },
					{ text: "price", value: "price" },
					{ text: "Popular season", value: "seasonDay" },
					{ text: "Store address", value: "address" },
				],
				property_product_headers: [
					{ text: "Name", value: "name" },
					{ text: "Product ID", value: "product_type_id" },
					{ text: "price", value: "price" },
					{ text: "Popular season", value: "seasonDay" },
					{ text: "Has neural model", value: "lstm" },
				],

				store_data: [
					{
						name: "Магазин 1",
						address: "Тимура фрунзе, 4",
						longtitude: 0,
						latitude: 0,
						fullness: 30,
						capacity: 14,
						minimum: 10,
						point_id: 1,
						productArr: [
							{
								name: "Bread",
								product_type_id: "976254762954",
								price: 10,
								seasonDay: 365,
								lstm: true,
							},
							{
								name: "Bread",
								product_type_id: "29654776592",
								price: 20,
								seasonDay: 365,
								lstm: true,
							},
							{
								name: "Bread",
								product_type_id: "79652457962",
								price: 50,
								seasonDay: 365,
								lstm: true,
							},
							{
								name: "Bread",
								product_type_id: "786542729654",
								price: 80,
								seasonDay: 365,
								lstm: true,
							},
						],
					},
					{
						name: "Магазин 2",
						address: "Проспект мира, 8б",
						longtitude: 0,
						latitude: 0,
						fullness: 80,
						capacity: 27,
						minimum: 15,
						point_id: 2,
						productArr: [
							{
								name: "Bread",
								product_type_id: "3769539765",
								price: 60,
								seasonDay: 365,
								lstm: true,
							},
							{
								name: "Butter",
								product_type_id: "93796",
								price: 11,
								seasonDay: 365,
								lstm: true,
							},
							{
								name: "Milk",
								product_type_id: "39767396",
								price: 34,
								seasonDay: 365,
								lstm: true,
							},
							{
								name: "???",
								product_type_id: "265848625",
								price: 66,
								seasonDay: 365,
								lstm: true,
							},
							{
								name: "",
								product_type_id: "268862",
								price: 0,
								seasonDay: 365,
								lstm: true,
							},
						],
					},
				],
				product_items: [],
				property_items: [],
			};
		},
		created() {
			axios.get("http://127.0.0.1:5000/api/locations").then((response) => {
				this.locations = response.data.locations;
			});
			axios
				.get("http://127.0.0.1:5000/api/product_types", {
					Authorization: localStorage.getItem("token") || "",
				})
				.then((response) => {
					this.product_items = response.data.product_types;
				});

			axios
				.post("http://127.0.0.1:5000/api/user/integrate", {
					Authorization: localStorage.getItem("token") || "",
				})
				.then((response) => {
					this.property_items = response.data;
				});

			console.log(this.product_items);
		},
	};
</script>
