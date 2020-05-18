<template>
	<div>
		<yandex-map :zoom="12.5" :coords="[55.753, 37.62]" :controls="[]" style="width: 700px; height: 700px;" :placemarks="placemarks" @map-was-initialized="initHandler">
			<ymap-marker marker-type="circle" :coords="[55.753, 37.62]" circle-radius="4500" hint-content="Zone" marker-id="0" :marker-fill="{ color: '#000', opacity: 0 }" :marker-stroke="{ color: '#ff0000', width: 200, opacity: 0.5 }" :balloon="{ header: 'Это зона', body: 'вы в зоне', footer: 'Урона нет' }"></ymap-marker>
			<ymap-marker marker-type="circle" :coords="[55.765, 37.6]" circle-radius="700" hint-content="Cool loot zone" marker-id="1" :marker-fill="{ color: '#00FFFF', opacity: 0.5 }" :balloon="{ header: 'Cool loot', body: 'Probability of high loot here is increased' }"></ymap-marker>
			<ymap-marker marker-type="circle" :coords="[55.75, 37.63]" circle-radius="1500" hint-content="Next zone" marker-id="2" :marker-fill="{ color: '#D8D8D8', opacity: 0.3 }" :balloon="{ header: 'Next zone' }" :marker-stroke="{ color: '#808080', width: 2, opacity: 1 }"></ymap-marker>
			<ymap-marker :coords="[55.745, 37.6]" marker-id="3" hint-content="That's you" :icon="markerIcon" />
			<ymap-marker :coords="[55.755, 37.59]" marker-id="4" hint-content="Store" :icon="storeIcon" />
			<ymap-marker :coords="[55.755, 37.63]" marker-id="4" hint-content="Store" :icon="storeIcon" />
		</yandex-map>
	</div>
</template>

<script>
	import { yandexMap, ymapMarker } from "vue-yandex-maps";

	export default {
		components: { yandexMap, ymapMarker },
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
					imageHref: "https://cdn.icon-icons.com/icons2/1706/PNG/512/3986701-online-shop-store-store-icon_112278.png",
					imageSize: [43, 43],
					imageOffset: [0, 0],
					contentOffset: [0, 15],
					contentLayout: '<div style="background: red; width: 50px; color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>',
				},
			};
		},
	};
</script>
