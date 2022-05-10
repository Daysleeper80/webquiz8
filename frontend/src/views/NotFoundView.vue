<template>
  <div>
        <p>Not Found: {{ $route.params.notFoundPathMatch  }}</p> 
    <!-- 
        OU
       <p>Not Found: {{ notFoundPathMatch  }}</p>

        E ali em cima precisamos de um script setup c/ defineProps para
        notFoundPathMatch. Por exemplo:

            <script setup>
            defineProps({
                notFoundPathMatch: {
                    type: String,
                    default: '/',
                }
            });
            </script>

        Além de que a rota precisa de ser marcada com props: true.
    -->
  </div>
</template>
