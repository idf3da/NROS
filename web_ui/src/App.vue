<template>
	<v-app id="web_ui">
		<v-app-bar app clipped-left dense flat hide-on-scrol overlap>
			<v-img
				src="projectIconWhite.png"
				max-height="40"
				max-width="40"
				contain
			></v-img>
			<v-toolbar-title>NROS</v-toolbar-title>
			<v-spacer></v-spacer>

			<v-menu absolute offset-y close-on-click transition="scale-transition">
				<template
					v-slot:activator="{
						on
					}"
				>
					<v-btn
						text
						@click.stop="
							notifocationsListExpanded = !notifocationsListExpanded
						"
						dark
						v-on="on"
					>
						<v-badge overlap color="green" :content="notificationBadgeNum">
							<v-icon>mdi-bell </v-icon>
						</v-badge>
					</v-btn>
				</template>

				<v-list>
					<v-list-item
						link
						dense
						v-for="(userMenuItem, index) in notificationItems"
						:key="index"
						router
						:to="userMenuItem.link"
					>
						<v-list-item-title>{{ userMenuItem.title }}</v-list-item-title>
					</v-list-item>
				</v-list>
			</v-menu>

			<v-menu offset-y close-on-click>
				<template
					v-slot:activator="{
						on
					}"
				>
					<v-btn
						text
						color="red"
						@click.stop="userMenuExpanded = !userMenuExpanded"
						dark
						v-on="on"
					>
						User name
						<v-icon right>{{ changeArrowOnExpandUserMenu }}</v-icon>
					</v-btn>
				</template>

				<v-list>
					<v-list-item
						link
						dense
						v-for="(notificationItem, index) in userMenuItems"
						:key="index"
						router
						:to="notificationItem.link"
					>
						<v-list-item-title>{{
							notificationItem.title
						}}</v-list-item-title>
					</v-list-item>
					<v-list-item link dense router>
						<v-list-item-title @click="logOutSnackbar = true"
							>Log out</v-list-item-title
						>
					</v-list-item>
				</v-list>
			</v-menu>
		</v-app-bar>

		<v-navigation-drawer
			mini-variant-width="50px"
			app
			clipped
			permanent
			v-bind:mini-variant="drawerExpanded"
			floating
			width="170px"
		>
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

		<v-snackbar v-model="logOutSnackbar" timeout="3000">
			{{ logOutSnackbarText }}
			<v-btn color="pink" text @click="logOutSnackbar = false">
				Close
			</v-btn>
		</v-snackbar>

		<v-footer hide app absolute>
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
			logOutSnackbar: false,
			notifocationsListExpanded: true,
			logOutSnackbarText: "You have logged out.",
			userMenuItems: [
				{
					title: "Profile",
					link: "/profile"
				},
				{
					title: "Settings",
					link: "/settings"
				}
			],
			notificationItems: [
				{
					title: "Notification 1",
					link: "/notifications/1"
				},
				{
					title: "Notification 2",
					link: "/notifications/2"
				}
			]
		}),
		created() {
			this.$vuetify.theme.dark = true;
		},
		computed: {
			changeArrowOnExpandDrawer: function() {
				return this.drawerExpanded === true
					? "mdi-arrow-right"
					: "mdi-arrow-left";
			},
			changeArrowOnExpandUserMenu: function() {
				return this.userMenuExpanded === true ? "mdi-menu-down" : "mdi-menu-up";
			},
			notificationBadgeNum: function() {
				return this.notificationItems.length;
			}
		}
	};
</script>
