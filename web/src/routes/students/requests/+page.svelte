<script lang="ts">
	import type { userSchema } from '$lib/schemas';
	import { watch } from 'runed';
	import { z } from 'zod';

	const schema = z.object({
		offer_id: z.string(),
		mentor_id: z.string(),
		user_id: z.string(),
		message: z.string(),
		date: z.date()
	});

	type Type = z.infer<typeof schema>;
	type User = z.infer<typeof userSchema>;

	let isMentor: boolean | undefined = $state(false);

	let token: string | null = localStorage.getItem('token');
	let user: User | undefined = $state();
	let data: Type | undefined = $state();

	let promise: any = $state();
	if (token) {
		promise = fetch('https://prod-team-35-lg7sic6v.REDACTED/api/user/profile', {
			method: 'GET',
			headers: {
				authorization: 'Bearer ' + token
			}
		}).then(async (response) => {
			if (response.ok) {
				const responseJson = await response.json();
				user = responseJson;
				isMentor = user?.is_mentor;
			}
		});
	}

	let requestsList: Type[] = $state([]);

	const changeOfferStatus = (index: number, status: boolean) => {
		fetch(
			'https://prod-team-35-lg7sic6v.REDACTED/api/mentors/offers/' +
				requestsList[index].offer_id,
			{
				method: 'POST',
				headers: {
					'Content-type': 'application/json; charset=UTF-8',
					authorization: 'Bearer ' + token
				},
				body: JSON.stringify({ status: status })
			}
		).then(async (response) => {
			if (response.ok) {
				let answeredReqs: string | null = localStorage.getItem('answered-reqs');
				if (!answeredReqs) answeredReqs = '[]';
				let answeredReqsList: Array<string | null> | null = JSON.parse(answeredReqs);
				const responseJson = await response.json();
				answeredReqsList?.push(responseJson.offer_id);
				localStorage.setItem('answered-reqs', JSON.stringify(answeredReqsList));
			}
		});
	};

	watch(
		() => isMentor,
		() => {
			if (!isMentor) {
				window.location.href = '/';
			} else {
				fetch('https://prod-team-35-lg7sic6v.REDACTED/api/mentors/offer', {
					method: 'GET',
					headers: {
						authorization: 'Bearer ' + token
					}
				}).then(async (response) => {
					if (response.ok) {
						const responseJson = await response.json();
						requestsList = responseJson;
					}
				});
			}
		}
	);
</script>

{#if isMentor}
	<h1>Список заявок на ваше менторство</h1>
	{#if requestsList && requestsList.length !== 0}
		<ul>
			{#each requestsList as req, i}
				<li>
					<p>
						<b>От пользователя с <i>user_id</i>:</b>
						{req.user_id} <br />
						<b>Дата создания:</b>
						{new Date(req.date)}
					</p>
					<div class="row">
						<input
							type="button"
							value="Отклонить"
							class="red"
							onclick={() => {
								changeOfferStatus(i, false);
							}}
						/>
						<input
							type="button"
							value="Принять"
							class="green"
							onclick={() => {
								changeOfferStatus(i, true);
							}}
						/>
					</div>
				</li>
			{/each}
		</ul>
	{/if}
{/if}

<style>
	ul {
		margin-left: 0;
	}

	li {
		list-style: none;
	}
</style>
