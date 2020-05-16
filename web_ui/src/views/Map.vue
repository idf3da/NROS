<template>
	<div>
		<yandex-map :zoom="12.5" :coords="[55.753, 37.62]" :controls="[]" style="width: 600px; height: 600px;" :placemarks="placemarks" @map-was-initialized="initHandler">
			<ymap-marker marker-type="circle" :coords="[55.753, 37.62]" circle-radius="4500" hint-content="Zone" marker-id="0" :marker-fill="{ color: '#000', opacity: 0 }" :marker-stroke="{ color: '#ff0000', width: 200, opacity: 0.5 }" :balloon="{ header: 'Это зона', body: 'вы в зоне', footer: 'Урона нет' }"></ymap-marker>
			<ymap-marker marker-type="circle" :coords="[55.765, 37.6]" circle-radius="700" hint-content="Cool loot zone" marker-id="1" :marker-fill="{ color: '#00FFFF', opacity: 0.5 }" :balloon="{ header: 'Cool loot', body: 'Probability of high loot here is increased' }"></ymap-marker>
			<ymap-marker marker-type="circle" :coords="[55.75, 37.63]" circle-radius="1500" hint-content="Next zone" marker-id="2" :marker-fill="{ color: '#D8D8D8', opacity: 0.3 }" :balloon="{ header: 'Next zone' }" :marker-stroke="{ color: '#808080', width: 2, opacity: 1 }"></ymap-marker>
		</yandex-map>
	</div>
</template>

<script>
	import { yandexMap, ymapMarker } from "vue-yandex-maps";

	export default {
		components: { yandexMap, ymapMarker },
	};
</script>
