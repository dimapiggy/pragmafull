<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';

import type { IOnboardingForm } from '~/types/auth';

import Step1 from '~/components/Pages/Auth/Step1.vue';
import Step2 from '~/components/Pages/Auth/Step2.vue';
import Step3 from '~/components/Pages/Auth/Step3.vue';
import Step4 from '~/components/Pages/Auth/Step4.vue';
import Step5 from '~/components/Pages/Auth/Step5.vue';
import Step6 from '~/components/Pages/Auth/Step6.vue';
import Step7 from '~/components/Pages/Auth/Step7.vue';
import Step8 from '~/components/Pages/Auth/Step8.vue';

definePageMeta({
  layout: 'not-auth',
});

useHead({
  title: 'Pragma',
  meta: [
    { name: 'description', content: 'Pragma' },
  ],
});

const authStore = useAuthStore();

const step = ref(1);

const form = ref<IOnboardingForm>({
  fullname: authStore.user?.fullname || '',
  task_creation_type: authStore.user?.task_creation_type || 'quick',
  notifications_enabled: authStore.user?.notifications_enabled || false,
  notification_time: authStore.user?.notification_time || '09:00:00',
  assistantStyle: 'restrained',
  assistantStyles: ['restrained', 'friendly'],
  inputTypes: ['quick', 'detailed'],
});

const currentStepComponent = computed(() => {
  if (step.value === 1) {
    return Step1;
  } else if (step.value === 2) {
    return Step2;
  } else if (step.value === 3) {
    return Step3;
  } else if (step.value === 4) {
    return Step4;
  } else if (step.value === 5) {
    return Step5;
  } else if (step.value === 6) {
    return Step6;
  } else if (step.value === 7) {
    return Step7;
  } else if (step.value === 8) {
    return Step8;
  }

  return 'div';
});

watch(step, () => scrollTop());

async function saveUser() {
  try {
    const userData = {
      fullname: form.value.fullname,
      task_creation_type: form.value.task_creation_type,
      notifications_enabled: form.value.notifications_enabled,
      notification_time: form.value.notification_time,
      assistantStyle: form.value.assistantStyle,
    };

    await authStore.registerUser(userData);

    setTimeout(() => {
      window.location.reload();
    }, 100);
  } catch (error) {
    console.error('Error saving user data:', error);
  }
}
</script>

<template>
  <div class="onbording">
    <component
      :is="currentStepComponent"
      v-model="step"
      v-model:form="form"
      @save-user="saveUser"
    />
  </div>
</template>

<style lang="scss">
.onbording {
  font-family: 'Mulish';
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - $headerheight);
  padding: 15px;
  box-sizing: border-box;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 18px;
  color: $mainblue;
}

.onbording > * {
  flex: 1;
}

.onbording div .blue-button {
  font-weight: 700;
}

.onb__wrapper {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  gap: 25px;
}

.onb__header {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 10px;
  margin-bottom: 30px;
}

.onb__header h1 {
  text-align: left;
  font-weight: bold;
  font-size: 24px;
  line-height: 120%;
  color: $mainblue;
  width: 100%;
}

.intro {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  gap: 10px;
}

.intro h2 {
  color: $mainblue;
  font-weight: 600;
  font-style: SemiBold;
  font-size: 20px;
  leading-trim: NONE;
  line-height: 120%;
  letter-spacing: 2%;
}

.intro__title {
  font-size: 20px;
  color: $mainblue;
  text-align: left;
  width: 100%;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
  width: 100%;
}

.step-number {
  font-size: 64px;
  font-weight: 1000;
  color: white;
  -webkit-text-stroke: 3px black;
  text-stroke: 3px black;
  line-height: 1;
}

.onb__buttons {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 300px;
  align-items: center;
  margin-bottom: 40px;
  gap: 16px;
}

.intro__text,
.intro__text p {
  font-weight: 400;
  font-style: Regular;
  font-size: 16px;
  leading-trim: NONE;
  line-height: 120%;
  letter-spacing: 2%;
  width: 100%;
}

.intro__point {
  position: relative;
  padding-left: 20px;
  text-align: left;
  line-height: 140%;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 6px;
    height: 6px;
    background-color: $mainblue;
    border-radius: 50%;
  }
}

.intro__points {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
}
</style>
