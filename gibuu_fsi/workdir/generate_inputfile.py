import uproot
import numpy as np
import sys


file=uproot.open("/path_to_workdir/jg_test_NIWG_dnn.root")

tree = file['NIWGTree']

nu_index = tree['NIWGEvent/nu_index'].array()
isnuc_index = tree['NIWGEvent/isnuc_index'].array()
fslep_index = tree['NIWGEvent/fslep_index'].array()
Q2_array = tree['NIWGEvent/Q2'].array()
p_array = tree['NIWGEvent/part_stack/part_stack.p'].array()
pdg_array= tree[ 'NIWGEvent/part_stack/part_stack.pdg'].array()
isatPV=tree[ 'NIWGEvent/part_stack/part_stack.isAtPrimaryVertex'].array() ## parent


# Split momentum and energy
fE = p_array['fE']
fPx = p_array['fP']['fX']
fPy = p_array['fP']['fY']
fPz = p_array['fP']['fZ']

mN = 0.938  # Nucleon mass



def moma(idx, j):
    return np.array([
        fE[j, idx],
        fPx[j, idx],
        fPy[j, idx],
        fPz[j, idx]
    ])


def beta(a, b):
    return (a[1:4] + b[1:4]) / (a[0] + b[0])


def lorentz_boost(beta_vec, four_vector):
    beta_vec = np.asarray(beta_vec, dtype=np.float64)
    four_vector = np.asarray(four_vector, dtype=np.float64)

    beta_squared = np.dot(beta_vec, beta_vec)

    if beta_squared < 1e-20:
        return four_vector.copy()
    if beta_squared >= 1.0:
        raise ValueError(f"(1 - beta^2) <= 0: {1.0 - beta_squared}\nbeta = {beta_vec}")

    gamma = 1.0 / np.sqrt(1.0 - beta_squared)
    beta_dot_p = np.dot(beta_vec, four_vector[1:4])

    spatial = four_vector[1:4] + gamma * beta_vec * ((gamma / (gamma + 1.0)) * beta_dot_p - four_vector[0])
    energy = gamma * (four_vector[0] - beta_dot_p)

    boosted = np.empty(4)
    boosted[0] = energy
    boosted[1:4] = spatial
    return boosted


def rotateZY(theta, phi, v_in, cosTheta=None):
    v_in = np.asarray(v_in, dtype=np.float64)

    if cosTheta is not None:
        cosT = cosTheta
        sinT = np.sqrt(max(1.0 - cosT**2, 0.0))
    else:
        cosT = np.cos(theta)
        sinT = np.sin(theta)

    cosP = np.cos(phi)
    sinP = np.sin(phi)

    RotMatrix = np.array([
        [ cosT*cosP, -sinP, sinT*cosP],
        [ cosT*sinP,  cosP, sinT*sinP],
        [   -sinT  ,   0. ,    cosT ]
    ])

    return RotMatrix @ v_in


def generate_fortran_assignment(j):
    nu_idx = nu_index[j]
    nuc_idx = isnuc_index[j]
    lep_idx = fslep_index[j]
    isatPV_idx=isatPV[j]
    if np.sum(isatPV_idx)==5:
        realparticle_external = moma(nuc_idx, j)
        realparticle_vel = realparticle_external[1:4] / realparticle_external[0]
        
        finalstate_external1 = moma(nuc_idx + 2, j)
        finalstate_external2=moma(nuc_idx+3,j)

        external_lepton_in = moma(nu_idx, j)
        external_lepton_out = moma(lep_idx, j)

        boson = external_lepton_in - external_lepton_out
        finalstate_external1= boson + realparticle_external
        finalstate_external2 = np.array([0., 0., 0., 0.])  # unused
        Q2 = Q2_array[j]

        def invariant_mass(vec1, vec2, vec3):
            total = vec1 - vec2 + vec3
            return np.sqrt(total[0]*total[0]-total[1]*total[1]-total[2]*total[2]-total[3]*total[3])

        W = invariant_mass(moma(nu_idx, j), moma(lep_idx, j), moma(nuc_idx, j))
        W_free = W
        W_rec = mN**2 + 2.*mN*(external_lepton_in[0] - external_lepton_out[0]) - Q2

        betacm = beta(moma(nuc_idx, j), boson)
        pcm = -lorentz_boost(betacm, realparticle_external)

        phi = np.arctan2(pcm[2], pcm[1])
        theta = np.arctan2(np.sqrt(pcm[1]**2 + pcm[2]**2), pcm[3])

        pB = lorentz_boost(betacm, external_lepton_in)
        pB[1:4] = rotateZY(theta, phi, pB[1:4])
        phiLepton = np.arctan2(pB[2], pB[1])
        if (pdg_array[j,nuc_idx]==2112):
            lines = [
                f"{realparticle_external[0]} {realparticle_external[1]} {realparticle_external[2]} {realparticle_external[3]}",
                f"{realparticle_vel[0]} {realparticle_vel[1]} {realparticle_vel[2]}",
                f"{finalstate_external1[0]} {finalstate_external1[1]} {finalstate_external1[2]} {finalstate_external1[3]}",
                f"{finalstate_external2[0]} {finalstate_external2[1]} {finalstate_external2[2]} {finalstate_external2[3]}",
                f"{external_lepton_in[0]} {external_lepton_in[1]} {external_lepton_in[2]} {external_lepton_in[3]}",
                f"{external_lepton_out[0]} {external_lepton_out[1]} {external_lepton_out[2]} {external_lepton_out[3]}",
                f"{boson[0]} {boson[1]} {boson[2]} {boson[3]}",
                f"{Q2}",
                f"{W}",
                f"{W_free}",
                f"{W_rec}",
                f"{pcm[0]} {pcm[1]} {pcm[2]} {pcm[3]}",
                f"{betacm[0]} {betacm[1]} {betacm[2]}",
                f"{phiLepton}",
                f"{1} {0} {0} {0} {2} {1}",  # static line
                f"{2}"
            ]
            
        else:
            lines = [
                f"{realparticle_external[0]} {realparticle_external[1]} {realparticle_external[2]} {realparticle_external[3]}",
                f"{realparticle_vel[0]} {realparticle_vel[1]} {realparticle_vel[2]}",
                f"{finalstate_external1[0]} {finalstate_external1[1]} {finalstate_external1[2]} {finalstate_external1[3]}",
                f"{finalstate_external2[0]} {finalstate_external2[1]} {finalstate_external2[2]} {finalstate_external2[3]}",
                f"{external_lepton_in[0]} {external_lepton_in[1]} {external_lepton_in[2]} {external_lepton_in[3]}",
                f"{external_lepton_out[0]} {external_lepton_out[1]} {external_lepton_out[2]} {external_lepton_out[3]}",
                f"{boson[0]} {boson[1]} {boson[2]} {boson[3]}",
                f"{Q2}",
                f"{W}",
                f"{W_free}",
                f"{W_rec}",
                f"{pcm[0]} {pcm[1]} {pcm[2]} {pcm[3]}",
                f"{betacm[0]} {betacm[1]} {betacm[2]}",
                f"{phiLepton}",
                f"{1} {1} {0} {0} {2} {2}",
                f"{2}"  
            ]
        return '\n'.join(lines)
    else:
        realparticle_external = moma(nuc_idx, j)
        realparticle_vel = realparticle_external[1:4] / realparticle_external[0]

        finalstate_external1 = moma(nuc_idx + 2, j)
        finalstate_external2 = np.array([0., 0., 0., 0.])  # unused

        external_lepton_in = moma(nu_idx, j)
        external_lepton_out = moma(lep_idx, j)

        boson = external_lepton_in - external_lepton_out
        Q2 = Q2_array[j]

        def invariant_mass(vec1, vec2, vec3):
            total = vec1 - vec2 + vec3
            return np.sqrt(total[0]*total[0]-total[1]*total[1]-total[2]*total[2]-total[3]*total[3])

        W = invariant_mass(moma(nu_idx, j), moma(lep_idx, j), moma(nuc_idx, j))
        W_free = W
        W_rec = mN**2 + 2.*mN*(external_lepton_in[0] - external_lepton_out[0]) - Q2

        betacm = beta(moma(nuc_idx, j), boson)
        pcm = -lorentz_boost(betacm, realparticle_external)

        phi = np.arctan2(pcm[2], pcm[1])
        theta = np.arctan2(np.sqrt(pcm[1]**2 + pcm[2]**2), pcm[3])

        pB = lorentz_boost(betacm, external_lepton_in)
        pB[1:4] = rotateZY(theta, phi, pB[1:4])
        phiLepton = np.arctan2(pB[2], pB[1])

        lines = [
            f"{realparticle_external[0]} {realparticle_external[1]} {realparticle_external[2]} {realparticle_external[3]}",
            f"{realparticle_vel[0]} {realparticle_vel[1]} {realparticle_vel[2]}",
            f"{finalstate_external1[0]} {finalstate_external1[1]} {finalstate_external1[2]} {finalstate_external1[3]}",
            f"{finalstate_external2[0]} {finalstate_external2[1]} {finalstate_external2[2]} {finalstate_external2[3]}",
            f"{external_lepton_in[0]} {external_lepton_in[1]} {external_lepton_in[2]} {external_lepton_in[3]}",
            f"{external_lepton_out[0]} {external_lepton_out[1]} {external_lepton_out[2]} {external_lepton_out[3]}",
            f"{boson[0]} {boson[1]} {boson[2]} {boson[3]}",
            f"{Q2}",
            f"{W}",
            f"{W_free}",
            f"{W_rec}",
            f"{pcm[0]} {pcm[1]} {pcm[2]} {pcm[3]}",
            f"{betacm[0]} {betacm[1]} {betacm[2]}",
            f"{phiLepton}",
            f"{1} {0} {1} {0} {1} {1}",  # static line
            f"{1}"
        ]
        return '\n'.join(lines)

def write_fortran_include(j, filename="input_values.f90"):
    fortran_code = generate_fortran_assignment(j)
    with open(filename, "w") as f:
        f.write(fortran_code)

# Usage
if __name__ == "__main__":
    i = int(sys.argv[1])
    write_fortran_include(i, filename=f"input_values{i}.f90")
        
