<template>
	<vs-root>
		<vs-row type="flex" vs-justify="center" vs-align="center" vs-w="12">
			<vs-card class="cardx">
				<div class="d-flex align-items-center dropdownbtn-alignment">
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
		</vs-row>

		<vs-row type="flex" vs-justify="center" vs-align="center">
			<vs-card class="cardx" fixedHeight vs-w="12">
				<div slot="media">
					<img src="@/assets/images/big/img1.jpg">
				</div>
			</vs-card>
		</vs-row>

		<vs-row vs-justify="center">
			<vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
				<vs-card class="cardx">
					alskjhd lksjh sfajkh asjfh lkasfh
				</vs-card>
			</vs-col>

			<vs-col type="flex" vs-justify="center" vs-align="center" vs-w="6">
				<vs-card class="cardx">
					alskjhd lksjh sfajkh asjfh lkasfh
				</vs-card>
			</vs-col>
		</vs-row>
	</vs-root>
</template>

<script>

export default {
	name: 'Index',
  components: {
  }
}
</script>
