
### **Smoke Test - Check list**

#### **1. Producer | Deploy the pipeline components**

 - [ ] All you need to do to deploy the multiple components is go to the `/smoke-test` folder that you'll have, and you'll have adapters and mappers (both for the producer and the consumer). 
 - [ ] Copy this `/adapter` into the `/adaptor` folder. 
 - [ ] Copy the producer mappers (the one for the schema assurance and the one to add the security labels) into the `/mappers` folder.
 - [ ] Once you've done this, and **assuming you have the Github actions/Azure DevOps in place** -, you're ready to get these components deployed. So push your changes and you should get the pipelines triggered.
 - [ ] After **pushing the changes** you should have **3 pipelines triggered**, and they were triggered. 
 - [ ] Once the pipelines are finished, you should have **3 ELM charts, one for the adapter and 2 for the other mappers**. These are the steps required to deploy the components on the producer side.

#### **2. Consumer | Deploy the pipeline components**

 - [ ] On the consumer side, we're gonna be doing the exact same thing we did on the producer side.
 - [ ] We're gonna copy the mapper responsible for extracting the data, paste it into this mapper's directory. After that, do the same thing for the mapper that is responsible for performing the schema assurance.
 - [ ] Once you've done this, you're ready to get these  components deployed _i.e._ **push your changes and you should get the pipelines triggered**    .
 - [ ] Once the pipelines are finished, you should have **2 ELM charts**, one for the mapper responsible for extracting the data and one for the mapper that is responsible for performing the schema assurance.

#### **3. Update the flux repo**
 - [ ] After performing the steps above, we're now in conditions to update the flux repo accordingly. On the producer side, you'll need to update the version of the adapter and the mapper responsible for the scheme assurance.
 These version should be copied from the Container Registry.
 - [ ] Once you've done this, you're ready to push your changes on the flux repo.
 - [ ] Once you've push the data pipelines release, both on the consumer side and producer side, the k8s cluster should automatically create the components.
 - [ ] Once the components are created, you should get the data flowing from the producer to the consumer.

_Note_: Be mindful that, to get the components running smoothly, you'll need to **create the secrets** as the documentation of the DSI data pipelines suggests.
