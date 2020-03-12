<template>
	<div class="home">
		<v-row style="padding: 30px" class="mb-2" justify="center" no-gutters>
			<v-col>
				<v-card class="pa-6" outlined tile>
					1x1
				</v-card>
				<v-card class="pa-6" outlined tile>
					1x2
				</v-card>
			</v-col>
			<v-col>
				<v-card class="pa-6" outlined tile>
					2x1
				</v-card>
				<v-card class="pa-6" outlined tile>
					2x1
				</v-card>
			</v-col>
		</v-row>
	</div>
</template>
<script>
	import Vue from "vue";
	import { ChartPlugin, LineSeries, Category } from "@syncfusion/ej2-vue-charts";

	Vue.use(ChartPlugin);

	export default {
		data() {
			return {
				seriesData: [
					{ month: "Jan", sales: 35 },
					{ month: "Feb", sales: 28 },
					{ month: "Mar", sales: 34 },
					{ month: "Apr", sales: 32 },
					{ month: "May", sales: 40 },
					{ month: "Jun", sales: 32 },
					{ month: "Jul", sales: 35 },
					{ month: "Aug", sales: 55 },
					{ month: "Sep", sales: 38 },
					{ month: "Oct", sales: 30 },
					{ month: "Nov", sales: 25 },
					{ month: "Dec", sales: 32 }
				],
				primaryXAxis: {
					valueType: "Category"
				}
			};
		},
		provide: {
			chart: [LineSeries, Category]
		}
	};
</script>

<style>
	#container {
		height: 400px;
	}
</style>
