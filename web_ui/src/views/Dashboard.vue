<template>
	<div class="home">
		<v-dialog v-model="edit_dialog">
			<v-card>
				<v-card-title>
					<span class="headline">{{ formTitle }}</span>
				</v-card-title>

				<v-card-text>
					<v-container>
						<v-row>
							<v-col cols="12" sm="6" md="4">
								<v-text-field v-model="editedItem.name" disabled label="Name"></v-text-field>
							</v-col>
							<v-col cols="12" sm="6" md="4">
								<v-text-field v-model="editedItem.product_type_id" lable="Product type ID" disabled hide-details single-line label="ID"></v-text-field>
							</v-col>
							<v-col cols="12" sm="6" md="4">
								<v-text-field v-model="editedItem.sell_price" hide-details single-line label="Price" disabled></v-text-field>
							</v-col>
							<v-col cols="12" sm="6" md="4">
								<v-text-field v-model="editedItem.seasonality" hide-details single-line type="number" label="Season day"></v-text-field>
							</v-col>
							<v-col cols="12" sm="6" md="4">
								<v-checkbox v-model="editedItem.lstm" disabled label="Has lstm"></v-checkbox>
							</v-col>
							<v-col cols="12" sm="6" md="4">
								<v-text-field v-model="editedItem.fullness" hide-details single-line type="number" label="Fullness"></v-text-field>
							</v-col>
							<v-col cols="12" sm="6" md="4">
								<v-text-field v-model="editedItem.capacity" hide-details single-line type="number" label="Capacity"></v-text-field>
							</v-col>
							<v-col cols="12" sm="6" md="4">
								<v-text-field v-model="editedItem.minimum" hide-details single-line type="number" label="Minumum"></v-text-field>
							</v-col>
							<v-col cols="12" sm="6" md="4">
								<v-text-field v-model="editedItem.before_range" hide-details single-line type="number" label="Before range"></v-text-field>
							</v-col>
						</v-row>
					</v-container>
				</v-card-text>

				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
					<v-btn color="blue darken-1" text @click="save">Save</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>
		<v-container fluid>
			<v-row align="start" justify="space-around">
				<v-col>
					<v-card class="pa-1" outlined tile :loading="!product_items_loaded">
						<v-card-title class="mt-n2">
							Product Items
							<v-spacer></v-spacer>
							<v-text-field class="mt-n4" v-model="search1" append-icon="mdi-magnify" label="Search" hide-details></v-text-field>
						</v-card-title>
						<v-data-table :height="180" :headers="product_items_headers" :items="product_items" :search="search1">
							<template v-slot:item.actions="{ item }">
								<v-icon @click="send4training(item)">
									mdi-currency-usd
								</v-icon>
							</template>
						</v-data-table>
					</v-card>
				</v-col>
				<v-col>
					<v-card outlined tile>
						<v-card-text class="px-0 pa-0">
							<yandex-map disabled :zoom="13" :coords="[55.753, 37.62]" :controls="[]" style="height: 300px;" @map-was-initialized="initHandler">
								<ymap-marker :coords="[55.745, 37.6]" marker-id="3" hint-content="That's you" :icon="markerIcon" />
								<ymap-marker v-bind:key="item" :coords="item" :icon="storeIcon" v-for="item in store_coordinates"></ymap-marker>
							</yandex-map>
						</v-card-text>
					</v-card>
				</v-col>
				<v-responsive style="width: 100%"></v-responsive>
				<v-col>
					<v-card class="pa-0" outlined tile>
						<v-card-title class="mt-n2 mb-1">Products parameters</v-card-title>
						<v-divider></v-divider>
						<v-data-table class="mt-n3" :height="400" :headers="store_headers" :items="store_data" :single-expand="singleExpand" :expanded.sync="expanded_table" shop-key="point_id" show-expand :search="table_search" :options.sync="table_pagination" :loading="!store_data_loaded">
							<template v-if="store_data_loaded" v-slot:expanded-item="{ item }">
								<td :colspan="4">
									<v-data-table hide-default-footer :height="250" :headers="property_product_headers" :items="item.product_types" :option.sync="sub_table_pagination" elevation-0>
										<template v-slot:top>
											<v-toolbar flat>
												<v-toolbar-title caption>{{ each_store_products }}</v-toolbar-title>
											</v-toolbar>
										</template>
										<template v-slot:top>
											<v-toolbar flat>
												<v-toolbar-title>Products</v-toolbar-title>
											</v-toolbar>
										</template>
										<template v-slot:item.actions="{ item }">
											<v-icon small class="mr-2" @click="editItem(item)">
												mdi-pencil
											</v-icon>
											<v-icon small class="mr-2" @click="deleteItem(item)">
												mdi-delete
											</v-icon>
											<v-icon small @click="send4training(item)">
												mdi-check
											</v-icon>
										</template>
									</v-data-table>
								</td>
							</template>
						</v-data-table>
					</v-card>
				</v-col>
				<v-col v-if="store_data_loaded">
					<v-card style="width: 100%" class="pa-0" outlined tile>
						<v-card-title class="mt-n2 mb-1"
							>New predictions
							<v-spacer></v-spacer>
						</v-card-title>
						<v-data-table class="mt-n3" :height="400" :headers="prediction_headers" :items="predictions" iteam-key="product_type_id"> </v-data-table>
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
				singleExpand: true,
				editedProductIndex: -1,
				editedShopIndex: -1,
				store_data_loaded: false,
				table_pagination: {},
				expanded_table: [],
				search_prediction_product_id: "",
				expanded: [],
				edit_dialog: false,
				store_coordinates: [],
				product_items_loaded: false,
				editedItem: {
					name: "",
					product_type_id: 0,
					sell_price: 0,
					seasonality: 0,
					lstm: false,
					fullness: 0,
					capacity: 0,
					minimum: 0,
				},
				defaultItem: {
					name: "",
					product_type_id: 0,
					sell_price: 0,
					seasonality: 0,
					lstm: false,
					fullness: 0,
					capacity: 0,
					minimum: 0,
				},
				property_product_headers: [
					{ text: "Name", value: "name" },
					{ text: "Product ID", value: "product_type_id" },
					{ text: "Price", value: "sell_price" },
					{ text: "Popular season", value: "seasonality" },
					{ text: "Has neural model", value: "lstm" },
					{ text: "Fullness", value: "fullness" },
					{ text: "Capacity", value: "capacity" },
					{ text: "Before range", value: "before_range" },
					{ text: "Minimum", value: "minimum" },
					{ text: "Actions", value: "actions", sortable: false },
				],
				store_headers: [
					{ text: "Store ID", value: "point_id" },
					{ text: "Address", value: "address" },
					{ text: "Longtitude", value: "longitude" },
					{ text: "Latitude", value: "latitude" },
				],
				prediction_headers: [
					{ text: "Target product", value: "product_type_id" },
					{ text: "Store uantity", value: "shop_count" },
					{ text: "To store", value: "shop_id" },
					{ text: "From warehouse", value: "war_id" },
					{ text: "Warehouse quantity", value: "war_count" },
				],
				sub_table_pagination: [],
				table_selected: [],
				product_items_headers: [
					{ text: "Name", value: "name" },
					{ text: "Product ID", value: "id" },
					{ text: "Price", value: "price" },
					{ text: "Popular season", value: "seasonality" },
					{ text: "Actions", value: "actions", sortable: false },
				],

				store_data: [],
				product_items: [],
				property_items: [],
				prediction: [],
			};
		},
		created() {
			axios
				.get("http://127.0.0.1:5000/api/product_types", {
					Authorization: localStorage.getItem("token") || "",
				})
				.then((response) => {
					this.product_items = response.data.product_types;
					this.product_items_loaded = true;
				});
			axios
				.post("http://127.0.0.1:5000/api/user/integrate", {
					Authorization: localStorage.getItem("token") || "",
				})
				.then((response) => {
					this.store_data = response.data.result;
					this.store_data_loaded = true;
					for (let i = 0; i < this.store_data.length; i++) {
						for (let j = 0; j < this.store_data[i].product_types.length; j++) {
							this.store_data[i].product_types[j]["shop_index"] = i;
						}
						let coord = [this.store_data[i].latitude, this.store_data[i].longitude];
						this.store_coordinates.push(coord);
					}
				});
		},
		computed: {
			formTitle() {
				return this.editedProductIndex === -1 ? "New Item" : "Edit Item";
			},
		},
		watch: {
			edit_dialog(val) {
				val || this.close();
			},
		},
		methods: {
			editItem(item) {
				this.editedShopIndex = item["shop_index"];
				console.log(this.editedShopIndex, item, item["shop_index"]);
				this.editedProductIndex = this.store_data[this.editedShopIndex].product_types.indexOf(item);
				Object.assign(this.editedItem, this.store_data[this.editedShopIndex].product_types[this.editedProductIndex]);
				this.edit_dialog = true;
			},

			deleteItem(item) {
				this.editedShopIndex = item["shop_index"];
				var index = this.store_data[this.editedShopIndex].product_types.indexOf(item);
				this.store_data[this.editedShopIndex].product_types.splice(index, 1);
			},

			close() {
				this.edit_dialog = false;
				this.$nextTick(() => {
					this.editedItem = Object.assign({}, this.defaultItem);
					this.editedProductIndex = -1;
					this.editedShopIndex = -1;
				});
			},

			save() {
				Object.assign(this.store_data[this.editedShopIndex].product_types[this.editedProductIndex], this.editedItem);
				this.editStoreProduct(this.editedItem);
				this.close();
			},

			send4training(product) {
				axios
					.post("http://127.0.0.1:5000/api/lstms", {
						Authorization: localStorage.getItem("token") || "",
						before_range: product.before_range,
						point_id: product.point_id,
						product_type_id: product.product_type_id,
					})
					.then(function(response) {
						console.log(response);
					})
					.catch(function(error) {
						console.log(error);
					});
			},

			getPrediction(product) {
				axios
					.post("http://127.0.0.1:5000/api/lstms", {
						Authorization: localStorage.getItem("token") || "",
						product_type_id: product.product_type_id,
					})
					.then((response) => {
						this.prediction.push(response.data);
					});
			},

			editStoreProduct(product) {
				let store = this.store_data[product["shop_index"]];
				console.log("Index:", product["shop_index"], store, store["point_id"]);
				console.log(product.minimum, product.capacity, product.sell_price, product.fullness, store.point_id, product.product_type_id);
				console.log(localStorage.getItem("token"));
				axios
					.put("http://127.0.0.1:5000/api/tags", {
						Authorization: localStorage.getItem("token") || "",
						minimum: product.minimum,
						capacity: product.capacity,
						sell_price: product.sell_price,
						fullness: product.fullness,
						point_id: store.point_id,
						product_type_id: product.product_type_id,
					})
					.then((response) => {
						this.prediction.push(response.data);
					});
			},
		},
	};
</script>
