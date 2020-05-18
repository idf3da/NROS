<template>
	<div class="home">
		<v-container fluid grid-list-md>
			<v-layout>
				<v-flex class="pr-3">
					<v-card dark outlined>
						<v-card>
							<v-card-title>
								Product Items
								<v-spacer></v-spacer>
								<v-text-field v-model="search" append-icon="mdi-magnify" label="Search" hide-details></v-text-field>
							</v-card-title>
							<v-data-table :headers="headers" :items="locations" :search="search"></v-data-table>
						</v-card>
					</v-card>

					<v-card dark outlined>
						<v-card-text class="px-0">
							<line-chart :height="300"></line-chart>
						</v-card-text>
					</v-card>
				</v-flex>

				<v-flex xs6>
					<v-card dark outlined>
						<v-card-text class="px-0">
							<yandex-map
								:zoom="13"
								:coords="[55.753, 37.62]"
								:controls="[]"
								style="height: 300px;"
								:placemarks="placemarks"
								@map-was-initialized="initHandler"
							>
								<ymap-marker
									marker-type="circle"
									:coords="[55.753, 37.62]"
									circle-radius="4500"
									hint-content="Zone"
									marker-id="0"
									:marker-fill="{ color: '#000', opacity: 0 }"
									:marker-stroke="{ color: '#ff0000', width: 200, opacity: 0.5 }"
									:balloon="{ header: 'Это зона', body: 'вы в зоне', footer: 'Урона нет' }"
								></ymap-marker>
								<ymap-marker
									marker-type="circle"
									:coords="[55.765, 37.6]"
									circle-radius="700"
									hint-content="Cool loot zone"
									marker-id="1"
									:marker-fill="{ color: '#00FFFF', opacity: 0.5 }"
									:balloon="{ header: 'Cool loot', body: 'Probability of high loot here is increased' }"
								></ymap-marker>
								<ymap-marker
									marker-type="circle"
									:coords="[55.75, 37.63]"
									circle-radius="1500"
									hint-content="Next zone"
									marker-id="2"
									:marker-fill="{ color: '#D8D8D8', opacity: 0.3 }"
									:balloon="{ header: 'Next zone' }"
									:marker-stroke="{ color: '#808080', width: 2, opacity: 1 }"
								></ymap-marker>
								<ymap-marker
									:coords="[55.745, 37.6]"
									marker-id="3"
									hint-content="That's you"
									:icon="markerIcon"
								/>
								<ymap-marker
									:coords="[55.755, 37.59]"
									marker-id="4"
									hint-content="Store"
									:icon="storeIcon"
								/>
								<ymap-marker
									:coords="[55.755, 37.63]"
									marker-id="4"
									hint-content="Store"
									:icon="storeIcon"
								/>
							</yandex-map>
						</v-card-text>
					</v-card>
				</v-flex>
			</v-layout>
		</v-container>
	</div>
</template>
<script>
import LineChart from "@/components/LineChart";
import { yandexMap, ymapMarker } from "vue-yandex-maps";
import axios from "axios";

export default {
	name: "VueChartJS",
	components: {
		LineChart,
		yandexMap,
		ymapMarker
	},
	data() {
		return {
			markerIcon: {
				layout: "default#imageWithContent",
				imageHref:
					"https://cdn2.iconfinder.com/data/icons/maps-navigation-glyph-black/614/3719_-_Pointer_I-512.png",
				imageSize: [43, 43],
				imageOffset: [0, 0],
				contentOffset: [0, 15],
				contentLayout:
					'<div style="background: red; width: 50px; color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>'
			},
			storeIcon: {
				layout: "default#imageWithContent",
				imageHref:
					"https://cdn.icon-icons.com/icons2/1706/PNG/512/3986701-online-shop-store-store-icon_112278.png",
				imageSize: [43, 43],
				imageOffset: [0, 0],
				contentOffset: [0, 15],
				contentLayout:
					'<div style="background: red; width: 50px; color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>'
			},
			search: "",
			headers: [
				{
					text: "Location Id",
					align: "start",
					value: "id"
				},
				{ text: "Address", value: "address" },
				{ text: "Latitude", value: "latitude" },
				{ text: "Longitude", value: "longitude" }
			],
			locations: []
		};
	},
	mounted() {
		axios.get("http://127.0.0.1:5000/api/locations").then(response => {
			this.locations = response.data.locations;
		});
	}
};
</script>