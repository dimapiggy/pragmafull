export interface IUser {
  id: number
  telegram_id: number
  username: string | null
  fullname: string
  task_creation_type: string
  notifications_enabled: boolean
  notification_time: string
}

export interface IUserPrefill {
  id?: number
  telegram_id?: number
  fullname: string
  task_creation_type: string
  notifications_enabled: boolean
  notification_time: string
}
