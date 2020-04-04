<template>
    <v-app id="inspire">
        <v-navigation-drawer v-model="drawer" app>
            <v-list dense>
                <v-list-item link @click.stop="drawer = !drawer" dense>
                    <v-list-item-action>
                        <v-icon>mdi-arrow-left</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Close</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link dense to="/main">
                    <v-list-item-action>
                        <v-icon>mdi-view-dashboard</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Main menu</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link dense to="/data_checker">
                    <v-list-item-action>
                        <v-icon>mdi-database</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Data Checker</v-list-item-title>
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
                <v-list-item link dense to="/settings">
                    <v-list-item-action>
                        <v-icon>mdi-settings</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Settings</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link dense to="/about">
                    <v-list-item-action>
                        <v-icon>mdi-file-document-box</v-icon>
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

        <v-app-bar app clipped-left>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
            <div>
                <v-toolbar-title>
                    Application
                </v-toolbar-title>
            </div>
            <v-tabs centered v-if="currentRouteName === 'DataChecker'">
                <v-tab link dense to="/data_checker/types">Types</v-tab>
                <v-tab link dense to="/data_checker/items">Items</v-tab>
                <v-tab link dense to="/data_checker/groups">Groups</v-tab>
                <v-tab link dense to="/data_checker/locations">Locations</v-tab>
            </v-tabs>
        </v-app-bar>

        <v-content>
            <router-view/>
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
            drawer: null
        }),
        created() {
            this.$vuetify.theme.dark = true;
        },
        computed: {
            currentRouteName: function () {
                return this.$route.name
            }
        }
    };
</script>
