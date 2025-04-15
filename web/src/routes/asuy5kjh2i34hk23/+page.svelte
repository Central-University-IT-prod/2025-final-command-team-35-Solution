<script lang="ts">
	import { watch } from 'runed';
	import { date, z } from 'zod';

	const mentorRequestSchema = z.object({
		request_id: z.string(),
		user_id: z.string(),
		about: z.string(),
		direction: z.string(),
		date: z.date(),
		status: z.boolean()
	});

	type MentorRequest = z.infer<typeof mentorRequestSchema>;

	let token: string | null = localStorage.getItem('token');
	let isAdmin = $state(false);

	let mentorRequests: MentorRequest[] | undefined = $state([]);
	let activeMentorRequests: MentorRequest[] | undefined = $derived.by(() => {
		if (mentorRequests) {
			return mentorRequests.filter((req) => !req.status);
		} else {
			return undefined;
		}
	});

	let promise: any = $state();
	if (token) {
		promise = fetch('https://prod-team-35-lg7sic6v.REDACTED/api/check', {
			method: 'POST',
			headers: {
				authorization: 'Bearer ' + token
			}
		}).then(async (response) => {
			if (response.ok) isAdmin = await response.json();
		});
	}

	let mentorRequestStatusPromise;
	const changeMentorRequestStatus = (mentorRequestIndex: number, status: boolean) => {
		mentorRequestStatusPromise = fetch(
			'https://prod-team-35-lg7sic6v.REDACTED/api/admin/secreturl/mentor-requests/' +
				mentorRequests![mentorRequestIndex].request_id,
			{
				method: 'POST',
				headers: {
					'Content-type': 'application/json; charset=UTF-8',
					authorization: 'Bearer ' + token
				},
				body: JSON.stringify({ status: status })
			}
		).then((response) => {
			if (response.ok) {
				mentorRequests![mentorRequestIndex].status = status;
			}
		});
	};

	watch(
		() => isAdmin,
		() => {
			if (isAdmin) {
				fetch(
					'https://prod-team-35-lg7sic6v.REDACTED/api/admin/secreturl/mentor-requests',
					{
						method: 'GET',
						headers: {
							authorization: 'Bearer ' + token
						}
					}
				).then(async (response) => {
					if (response.ok) {
						mentorRequests = await response.json();
					}
				});
			}
		}
	);
</script>

{#await promise}
	<h1>Проверка прав доступа</h1>
{:then}
	{#if isAdmin}
		<h1>Панель администратора</h1>
		<h3>Заявки на становления ментором</h3>
		{#if activeMentorRequests && activeMentorRequests.length !== 0}
			<p>{JSON.stringify(activeMentorRequests)}</p>
			<ul>
				{#each activeMentorRequests as req, i}
					<li>
						<p>
							<b>От пользователя с <i>user_id</i>:</b>
							{req.user_id} <br />
							<b>О пользователе:</b>
							{req.about} <br />
							<b>Специализация:</b>
							{req.direction} <br />
							<b>Дата создания:</b>
							{new Date(req.date)}
						</p>
						<div class="row">
							<input
								type="button"
								value="Отклонить"
								class="red"
								onclick={() => {
									changeMentorRequestStatus(i, false);
								}}
							/>
							<input
								type="button"
								value="Принять"
								class="green"
								onclick={() => {
									changeMentorRequestStatus(i, true);
								}}
							/>
						</div>
					</li>
				{/each}
			</ul>
		{:else}
			Заявки отсутствуют
		{/if}
	{:else}
		<h1>Этот дом запривачен, разворачивайся.</h1>
	{/if}
{:catch}
	<h1>Прод упал</h1>
{/await}

<style>
	ul {
		padding-left: 0;
	}

	li {
		list-style: none;
		padding: 1em;

		background-color: whitesmoke;
		border-radius: 0.5em;
	}

	.row {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		gap: 1em;
	}

	.row > * {
		width: 100%;
		border: none;
		margin-bottom: 0;
	}

	.green {
		background-color: #77b254;
	}

	.red {
		background-color: #be3144;
	}
</style>
