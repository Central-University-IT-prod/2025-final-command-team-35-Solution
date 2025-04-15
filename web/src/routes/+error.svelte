<script lang="ts">
	import { page } from '$app/stores';

	window.location.href = '/';
</script>

<h1>Что-то пошло не так.</h1>

<h4>Код ошибки:</h4>
<kbd>{$page.status}</kbd>

<h4>Текст ошибки:</h4>
<kbd>{$page.error?.message}</kbd>

<style>
	h4 {
		margin-bottom: 0.5em;
	}
	kbd {
		margin-bottom: 1em;
	}
</style>
