import { z } from 'zod';

export const userSchema = z.object({
	login: z
		.string()
		.min(3, 'Логин должен содержать минимум 3 символа')
		.max(20, 'Логин не должен превышать 20 символов')
		.optional(),
	password: z
		.string()
		.min(6, 'Пароль должен содержать минимум 6 символов')
		.max(50, 'Пароль не должен превышать 50 символов')
		.optional(),
	first_name: z
		.string()
		.min(2, 'Имя должно содержать минимум 2 символа')
		.max(50, 'Имя не должно превышать 50 символов'),
	last_name: z
		.string()
		.min(2, 'Фамилия должна содержать минимум 2 символа')
		.max(50, 'Фамилия не должна превышать 50 символов'),
	age: z
		.number()
		.int()
		.min(0, 'Возраст не может быть отрицательным')
		.max(120, 'Возраст не может превышать 120 лет'),
	about: z.string().max(500, 'Описание не должно превышать 500 символов').optional(),
	contact: z.string().max(100, 'Контактная информация не должна превышать 100 символов'),
	avatar: z.string().url('Аватар должен быть валидной ссылкой').optional(),
	is_mentor: z.boolean()
});

export const mentorSchema = z.object({
	mentor_id: z.string().uuid().optional(),
	first_name: z.string().optional(),
	last_name: z.string().optional(),
	age: z.number().int().min(0).max(125).optional(),
	direction: z.string().optional(),
	about: z.string().optional(),
	contact: z.string().optional()
});

export const mentorsArraySchema = z.array(mentorSchema);
