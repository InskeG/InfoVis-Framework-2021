<template>
	<vs-root>
		<div>
			<vs-navbar v-model="activeItem" class="nabarx">
			</vs-navbar>
		</div>

		<vs-col type="flex" vs-justify="center" vs-align="center" vs-lg="8">
			<vs-card class="cardx">
				<div class="d-flex align-items-center dropdownbtn-alignment" vs-lg="8">
					<vs-dropdown vs-trigger-click>
						<vs-button class="btn-alignment" type="filled" icon="expand_more">Pick a style!</vs-button>
						<vs-dropdown-menu>
							<vs-dropdown-item>
								option 1
							</vs-dropdown-item>
							<vs-dropdown-item>
								option 2
							</vs-dropdown-item>
							<vs-dropdown-item>
								option 3
							</vs-dropdown-item>
							<vs-dropdown-item>
								option 4
							</vs-dropdown-item>
						</vs-dropdown-menu>
					</vs-dropdown>
				</div>
			</vs-card>

			<vs-card class="cardx">
          <img src="@/assets/images/big/img1.jpg">
			</vs-card>

			<vs-row vs-justify="center">
				<vs-col type="flex" vs-justify="center" vs-align="center" vs-lg="6">
					<vs-card class="cardx">
						alskjhd lksjh sfajkh asjfh lkasfh
					</vs-card>
				</vs-col>
				<vs-col type="flex" vs-justify="center" vs-align="center" vs-lg="6">
					<vs-card class="cardx">
						alskjhd lksjh sfajkh asjfh lkasfh
					</vs-card>
				</vs-col>
			</vs-row>
		</vs-col>
	</vs-root>
</template>

<script>

export default {
	name: 'Index',
  components: {
  }
}
</script>
