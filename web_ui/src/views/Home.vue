<template>
	<div class="home">
		<v-row style="padding: 30px" class="mb-2" justify="center" no-gutters>
			<v-col>
				<v-card class="pa-6" outlined tile>
					1x1
					<line-chart></line-chart>
				</v-card>
				<v-card class="pa-6" outlined tile>
					1x2
					<bar-chart></bar-chart>
				</v-card>
			</v-col>
			<v-col>
				<v-card class="pa-6" outlined tile>
					2x1
					<bubble-chart></bubble-chart>
				</v-card>
				<v-card class="pa-6" outlined tile>
					2x1
					<reactive :chart-data="datacollection"></reactive>
					<button class="button is-primary" @click="fillData()">Randomize</button>
				</v-card>
			</v-col>
		</v-row>
	</div>
</template>
<script>
	import LineChart from "@/components/LineChart";
	import BarChart from "@/components/BarChart";
	import BubbleChart from "@/components/BubbleChart";
	import Reactive from "@/components/Reactive";

	export default {
		name: "VueChartJS",
		components: {
			LineChart,
			BarChart,
			BubbleChart,
			Reactive
		},
		data() {
			return {
				// instantiating datacollection with null
				datacollection: null
			};
		},
		created() {
			//anytime the vue instance is created, call the fillData() function.
			this.fillData();
		},
		methods: {
			fillData() {
				this.datacollection = {
					// Data for the y-axis of the chart
					labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
					datasets: [
						{
							label: "Data One",
							backgroundColor: "#f87979",
							// Data for the x-axis of the chart
							data: [this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt()]
						}
					]
				};
			},
			getRandomInt() {
				// JS function to generate numbers to be used for the chart
				return Math.floor(Math.random() * (50 - 5 + 1)) + 5;
			}
		}
	};
</script>

<style>
	#container {
		height: 400px;
	}
</style>
