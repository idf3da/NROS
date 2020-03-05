<template>
	<v-card
		class="mx-auto 
		text-center"
		color="green"
		dark
		max-width="600"
	>
		<v-card-text>
			<h2>Your stonks</h2>

			<v-sheet color="rgba(0, 0, 0, .12)">
				<v-catd-text>S&P 500</v-catd-text>
				<v-sparkline :value="valuesSP" color="white" height="100" padding="24" stroke-linecap="round" smooth>
					<template v-slot:label="item"> ${{ item.value }} </template>
				</v-sparkline>

				<v-divider dark inset light></v-divider>

				<v-catd-text>Vanguard US property</v-catd-text>
				<v-sparkline :value="valuesVP" color="white" height="100" padding="24" stroke-linecap="round" smooth>
					<template v-slot:label="item"> ${{ item.value }} </template>
				</v-sparkline>
			</v-sheet>
		</v-card-text>

		<v-card-text>
			<div
				class="display-1 
			font-weight-thin"
			>
				Week report
			</div>
		</v-card-text>

		<v-card-actions class="justify-center">
			<v-btn block text>Go full to Report?</v-btn>
		</v-card-actions>
		<h5>Better not to, cuz u r broke</h5>
	</v-card>
</template>

<script>
	export default {
		data: () => ({
			valuesSP: [750, 720, 610, 720, 446, 600, 0.01],
			valuesVP: [650, 920, 510, 750, 446, 300, 0.001]
		})
	};
</script>
