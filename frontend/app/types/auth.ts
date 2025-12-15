import type { IUser } from '~/types/user';

export type fetchUrlType = string | Request | Ref<string | Request> | (() => string | Request);

export interface IAuthResponse {
  success: boolean
  exists?: boolean
  user?: IUser
  access_token?: string
  refresh_token?: string

  prefill?: {
    id?: number
    telegram_id?: number
    username: string | null
    fullname: string
    task_creation_type: 'quick' | 'detailed' | string
    notifications_enabled: boolean
    notification_time: string
    assistantStyle?: 'restrained' | 'friendly' | string
  }
}

export interface IOnboardingForm {
  fullname: string
  task_creation_type: string
  notifications_enabled: boolean
  notification_time: string
  assistantStyle: string
  assistantStyles: string[]
  inputTypes: string[]
}
