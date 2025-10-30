export interface User {
  id: string;
  email: string;
  access_token?: string;
}

export interface CronJobStatus {
  id: string;
  user_id: string;
  status: 'idle' | 'running' | 'completed' | 'failed';
  user_logged: boolean;
  image_generated: boolean;
  content_generated: boolean;
  db_saved: boolean;
  uploaded_to_linkedin: boolean;
  error_message?: string;
  created_at: string;
  updated_at: string;
  linkedin_post_url?: string;
}

export interface JobStep {
  key: keyof Pick<CronJobStatus, 'user_logged' | 'image_generated' | 'content_generated' | 'db_saved' | 'uploaded_to_linkedin'>;
  label: string;
  description: string;
}
