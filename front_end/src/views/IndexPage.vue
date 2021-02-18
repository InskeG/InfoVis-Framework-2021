<template>
	<vs-root>
		<vs-row type="flex" vs-justify="center" vs-align="center">
			<vs-card class="cardx" v-if="fetched" fixedHeight vs-w="12">
				<div slot="media">
					<img src="@/assets/images/big/img1.jpg">
				</div>
			</vs-card>
		</vs-row>

		<vs-row vs-justify="center">
			<vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
				<vs-card class="cardx" v-if="fetched">
					<div slot="header"><h3>Interessante data</h3></div>
					<div>
						alskjhd lksjh sfajkh asjfh lkasfh
						alskjhd lksjh sfajkh asjfh lkasfh
						alskjhd lksjh sfajkh asjfh lkasfh
						alskjhd lksjh sfajkh asjfh lkasfh
						alskjhd lksjh sfajkh asjfh lkasfh
					</div>
				</vs-card>
				<vs-card class="cardx" v-if="fetched">
					<div slot="header"><h3>Meer statistieken</h3></div>
					<div>
						alskjhd lksjh sfajkh asjfh lkasfh
						Kijk deze krab nou. Zie hem krabben alsof er geen morgen is.
						Een ware inspiratie voor iedere liefhebber van geleedpotigen.
					</div>
				</vs-card>
			</vs-col>

			<vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
				<vs-card class="cardx" v-if="fetched">
					<div slot="header"><h3>{{ data.genre }} on Wikipedia</h3></div>
					<div>
						{{ data.summary }}
					</div>
				</vs-card>
			</vs-col>
		</vs-row>

		<vs-row type="flex" vs-justify="center" vs-align="center" vs-w="12">
			<vs-card class="cardx">
				<div slot="header"><h3>
                    Pick a <span v-if="fetched">new</span> style!
                </h3></div>
				<div class="d-flex align-items-center dropdownbtn-alignment">
					<vs-dropdown vs-trigger-click>
						<vs-button class="btn-alignment" type="filled" icon="expand_more">Pick a style!</vs-button>
						<vs-dropdown-menu>
							<vs-dropdown-item @click="get_info('Impressionism')">
								Impressionism
							</vs-dropdown-item>
							<vs-dropdown-item @click="get_info('Expressionism (fine arts)')">
								Expressionism
							</vs-dropdown-item>
							<vs-dropdown-item @click="get_info('Cubism')">
								Cubism
							</vs-dropdown-item>
							<vs-dropdown-item @click="get_info('Surrealism')">
								Surealism
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
            fetched: false,
		}
	},
  components: {
  },
	methods: {
		async get_info(genre) {
            this.$vs.loading();

			fetch("http://localhost:5000/info/" + genre + "/1993")
				.then(response => response.json())
				.then(data => {
					this.data = data;
					this.fetched = true;
                    this.$vs.loading.close()
				}
			);
		}
	}
}

</script>
