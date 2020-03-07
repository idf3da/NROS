<template>
	<v-app id="web_ui">
		<v-app-bar app clipped-left dense flat hide-on-scrol overlap>
			<v-img src="projectIconWhite.png" max-height="40" max-width="40" contain></v-img>
			<v-toolbar-title>NROS</v-toolbar-title>
			<v-spacer></v-spacer>

			<v-menu offset-y close-on-click>
				<template v-slot:activator="{ on }">
					<v-btn flat color="grey" @click.stop="userMenuExpanded = !userMenuExpanded" dark v-on="on"></v-btn>
					<v-icon left>{{ changeArrowOnExpandUserMenu }}</v-icon>
					<span>User name</span>
				</template>

				<v-list>
					<v-list-item link v-for="(item, index) in items" :key="index" router :to="item.link">
						<v-list-item-title>{{ item.title }}</v-list-item-title>
					</v-list-item>
				</v-list>
			</v-menu>

			<v-btn icon>
				<v-icon>mdi-magnify</v-icon>
			</v-btn>
		</v-app-bar>

		<v-navigation-drawer mini-variant-width="7%" app clipped permanent v-bind:mini-variant="drawerExpanded" floating width="25%">
			<v-list dense>
				<v-list-item link @click.stop="drawerExpanded = !drawerExpanded" dense>
					<v-list-item-action>
						<v-icon>{{ changeArrowOnExpandDrawer }}</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>Close</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
				<v-list-item link dense to="/main">
					<v-list-item-action>
						<v-icon>mdi-home-variant</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>Main menu</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
				<v-list-item link dense to="/charts">
					<v-list-item-action>
						<v-icon>mdi-chart-arc</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>Charts</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
				<v-list-item link dense to="/orders">
					<v-list-item-action>
						<v-icon>mdi-clipboard-arrow-right</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>Orders</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
				<v-list-item link dense to="/map">
					<v-list-item-action>
						<v-icon>mdi-map-marker-multiple</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>Map</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
				<v-list-item link dense to="/settings">
					<v-list-item-action>
						<v-icon>mdi-settings</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>Settings</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
				<v-list-item link dense to="/help">
					<v-list-item-action>
						<v-icon>mdi-help-circle</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>Help</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
				<v-list-item link dense to="/about">
					<v-list-item-action>
						<v-icon>mdi-border-all</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>About</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
				<v-list-item link dense disabled>
					<v-list-item-action>
						<v-icon>mdi-border-none</v-icon>
					</v-list-item-action>
					<v-list-item-content>
						<v-list-item-title>Disabled stuff</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
			</v-list>
		</v-navigation-drawer>

		<v-content>
			<router-view />
		</v-content>

		<v-footer app>
			<span>&copy; ME IRL&trade; </span>
		</v-footer>
	</v-app>
</template>

<script>
	export default {
		props: {
			source: String
		},
		data: () => ({
			drawerExpanded: true,
			userMenuExpanded: false,
			items: [{ title: "Profile", link: "/profile" }, { title: "Settings", link: "/settings" }, { title: "Log out" }]
		}),
		created() {
			this.$vuetify.theme.dark = true;
		},
		computed: {
			changeArrowOnExpandDrawer: function() {
				return this.drawerExpanded === true ? "mdi-arrow-right" : "mdi-arrow-left";
			},
			changeArrowOnExpandUserMenu: function() {
				return this.userMenuExpanded === true ? "mdi-arrow-down" : "mdi-arrow-up";
			}
		}
	};
</script>
