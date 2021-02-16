<template>
	<vs-root>

		<vs-row type="flex" vs-justify="center" vs-align="center">
			<vs-card class="cardx" v-if="data.fetched" fixedHeight vs-w="12">
				<div slot="media">
					<img src="@/assets/images/big/img1.jpg">
				</div>
			</vs-card>
		</vs-row>

		<vs-row vs-justify="center">
			<vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
				<vs-card class="cardx" v-if="data.fetched">
					<div slot="header"><h3>Interessante data</h3></div>
					<div>
						alskjhd lksjh sfajkh asjfh lkasfh
						alskjhd lksjh sfajkh asjfh lkasfh
						alskjhd lksjh sfajkh asjfh lkasfh
						alskjhd lksjh sfajkh asjfh lkasfh
						alskjhd lksjh sfajkh asjfh lkasfh
					</div>
				</vs-card>
				<vs-card class="cardx" v-if="data.fetched">
					<div slot="header"><h3>Meer statistieken</h3></div>
					<div>
						alskjhd lksjh sfajkh asjfh lkasfh
						Kijk deze krab nou. Zie hem krabben alsof er geen morgen is.
						Een ware inspiratie voor iedere liefhebber van geleedpotigen.
					</div>
				</vs-card>
			</vs-col>

			<vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
				<vs-card class="cardx" v-if="data.fetched">
					<div slot="header"><h3>About {{ data.genre }}</h3></div>
					<div>
						{{ data.info }}
					</div>
				</vs-card>
			</vs-col>
		</vs-row>

		<vs-row type="flex" vs-justify="center" vs-align="center" vs-w="12">
			<vs-card class="cardx">
				<div slot="header"><h3>Pick a style!</h3></div>
				<div class="d-flex align-items-center dropdownbtn-alignment">
					<vs-dropdown vs-trigger-click>
						<vs-button class="btn-alignment" type="filled" icon="expand_more">Pick a style!</vs-button>
						<vs-dropdown-menu>
							<vs-dropdown-item @click="get_info('kaas')">
								Kaas
							</vs-dropdown-item>
							<vs-dropdown-item @click="get_info('pindakaas')">
								Pindakaas
							</vs-dropdown-item>
							<vs-dropdown-item @click="get_info('worst')">
								Worst
							</vs-dropdown-item>
							<vs-dropdown-item @click="get_info('hagelslag')">
								Hagelslag
							</vs-dropdown-item>
						</vs-dropdown-menu>
					</vs-dropdown>
				</div>
			</vs-card>
		</vs-row>
	</vs-root>
</template>

<script>

export default {
	name: 'Index',
	data() {
		return {
			data: {
				fetched: false,
			}
		}
	},
  components: {
  },
	methods: {
		async get_info(genre) {
			const result = await fetch("http://192.168.0.108:8000/info/" + genre);
			const data = await result.json();
			this.data = data;
			this.data.genre = genre;
			this.data.fetched = true;
		}
	}
}

</script>
