<script setup>
import partition from 'lodash-es/partition';
import { format, compareAsc } from 'date-fns';

console.log(partition([1, 2, 3, 4], n => n % 2));

console.log(format(new Date(2014, 1, 11), 'MM/dd/yyyy'));
//=> '02/11/2014'

const dates = [
    new Date(1995, 6, 2),
    new Date(1987, 1, 11),
    new Date(1989, 6, 10),
];
dates.sort(compareAsc);
console.log(dates);

</script>

<template>
    <div class="about">
        <h1>This is an about page</h1>
        <button class="btn btn-primary" 
                data-bs-target="#collapseTarget" 
                data-bs-toggle="collapse"
                id="bootstrap-button">
            Bootstrap collapse example
        </button>
        <div class="collapse py-2" id="collapseTarget">
            This is the toggle-able content!
        </div>
    </div>
</template>

<style>
#bootstrap-button {
    margin: 1em;
}
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
