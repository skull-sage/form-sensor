import ovsLoggedUser from 'src/ovs-store/logged-user'

export default {
  computed : {
    loggedUser:()=> ovsLoggedUser.getLoggedUser()
  }
}
