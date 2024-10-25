import logging
import math
import operator
import random
import pandas as pd

import numpy as np

import westpa
from westpa.core.we_driver import WEDriver
from westpa.core.segment import Segment
from westpa.core.states import InitialState

log = logging.getLogger(__name__)

#energy=np.loadtxt("common_files/energy.dat",usecols=5)

temp_it=np.loadtxt("common_files/temp.dat")
pot_xs=np.loadtxt("common_files/pot.dat",usecols=0)
pot_ys=np.loadtxt("common_files/pot.dat",usecols=1)
                
#initial_nsegs=100
kb=0.002 ## boltzman constant, kcal.mol/K


class CustomDriver(WEDriver):
    def get_restart_auxdata(self, niter, field=None):
        # extract previous iteration data and add to curr_coords
        data_manager = westpa.rc.get_sim_manager().data_manager

        back_data = []
        with data_manager.lock:
            iter_group = data_manager.get_iter_group(niter)

            if field:
                data_raw = iter_group["auxdata/" + field][:]
            else:
                data_raw = iter_group["auxdata"][:]

            for seg in data_raw[:, 1:]:
                back_data.append(seg)

        return np.array(back_data)

    def get_prev_energies(self, iter):
        # extract previous iteration data and add to curr_coords
        data_manager = westpa.rc.get_sim_manager().data_manager
        with data_manager.lock:
                iter_group = data_manager.get_iter_group(iter)
                prev_ene = iter_group["auxdata/energy"][:]
        return prev_ene[:, -1]
    
    def _split_by_data(self, bin, to_split, split_into):

        if len(to_split) > 1:
            for segment, num in zip(to_split, split_into):
                bin.remove(segment)
                new_segments_list = self._split_walker(segment, num, bin)
                bin.update(new_segments_list)
        else:
            to_split = to_split[0]
            bin.remove(to_split)
            new_segments_list = self._split_walker(to_split, split_into[0], bin)
            bin.update(new_segments_list)


    def _merge_by_data(self, bin, to_merge):
        for group in to_merge:
            bin.difference_update(group)
            new_segment, parent = self._merge_walkers(group, None, bin)
            bin.add(new_segment)


    def _run_we(self):
        '''Run recycle/split/merge. Do not call this function directly; instead, use
        populate_initial(), rebin_current(), or construct_next().'''
        self._recycle_walkers()

        # sanity check
        self._check_pre()

        # dummy resampling block
        for bin in self.next_iter_binning:
            if len(bin) == 0:
                continue
            else:
                # this will allow you to get the pcoords for all frames
                current_iter_segments = self.current_iter_segments 
                curr_segments = np.array(sorted(current_iter_segments, key=operator.attrgetter('weight')), dtype=np.object_)
                seg_ids = list(map(operator.attrgetter('seg_id'), curr_segments))
                curr_pcoords = np.array(list(map(operator.attrgetter('pcoord'), curr_segments)))[:,:,0]
                init_check = curr_pcoords[:,0] != curr_pcoords[:,-1]                   

                key_function = lambda x: seg_ids.index(x.parent_id)

                segments = np.array(sorted(bin, key=key_function), dtype=np.object_)
                pcoords = np.array(list(map(operator.attrgetter('pcoord'), segments)))[:,:,0]
                pcoords = pcoords.reshape(pcoords.shape[0],pcoords.shape[1])                
                weights = np.array(list(map(operator.attrgetter('weight'), segments)))
                iters = np.array(list(map(operator.attrgetter('n_iter'), segments)))

                # Determining the current temperature based on the iteration
                real_it = iters[0]-1
                tf=temp_it[(real_it)][1]
                ti=temp_it[(real_it+1)][1]
                #dt=(tf/(300) - (ti/(300)))
                dt = ti - tf
                dt2 = ti**2 - tf**2
                print("\n ## IT", real_it, "temp current step", tf, "temp next step", ti, "delta T", dt, "\n")

                # Array for storing new weights after calculation
                new_weights = np.zeros((pcoords.shape[0]), dtype=float)
                
                # Reweighting
                if real_it > 1:

                    # Pull the final energy for the segments
                    try:
                        energies = np.array(list(seg.data['energy'] for seg in curr_segments))
                    except KeyError:
                        energies = self.get_restart_auxdata(real_it, 'energy')
                    
                    # Pull the final energy for the segments
                    try:
                        dih_energies = np.array(list(seg.data['dih_energy'] for seg in curr_segments))
                    except KeyError:
                        dih_energies = self.get_restart_auxdata(real_it, 'dih_energy')
                    try:
                        vdw_energies = np.array(list(seg.data['vdw_energy'] for seg in curr_segments))
                    except KeyError:
                        vdw_energies = self.get_restart_auxdata(real_it, 'vdw_energy')

                    try:
                        elec_energies = np.array(list(seg.data['elec_energy'] for seg in curr_segments))
                    except KeyError:
                        elec_energies = self.get_restart_auxdata(real_it, 'elec_energy')



                    cur_energies = energies[:, -1]
                    dih_energies = dih_energies[:, -1]
                    #dih_energies = energies[3,-1]
                    vdw_energies = vdw_energies[:,-1]
                    elec_energies = elec_energies[:,-1]
                    print(dih_energies)
                    print(vdw_energies)
                    print(elec_energies)
                    print(f"{len(new_weights)=}")
                    if real_it > 0:
                        # This is a method of getting the energies that uses the new lambda for calculation
                        # past_energies = energies[:, 0]
                        # Get the past energies
                        # past_energies = self.get_prev_energies(real_it - 1)
                        # print(past_energies)
                        # # Lambda function to sort by
                        # key_function = lambda x: seg_ids.index(x[0].parent_id)
                        # # Sort the zipped segments and energies using the 
                        # temp = sorted(zip(bin, past_energies), key=key_function)
                        # _, past_energies = map(list, zip(*temp))
                        # print(past_energies)
                
           
                        #d_ene = (dih_energies + vdw_energies)*(temp_it[(real_it)] - temp_it[(real_it+1)] ) + elec_energies*((temp_it[(real_it)])**2 - (temp_it[(real_it+1)] )**2)
                        potential = np.zeros(len(cur_energies), dtype=float)
  
                        for idx in range(len(cur_energies)):
                            # diff=np.abs(pot_xs-ival[0])
                    
                            potential[idx]=pot_ys[idx]
                            d_ene = dt*(dih_energies[idx] + vdw_energies[idx]) + dt2*elec_energies[idx]
                            new_weights[idx] = weights[idx]*np.exp(d_ene/(300*kb))
                            new_weights[idx] = new_weights[idx]*np.exp(np.log(potential[idx]/new_weights[idx]))

                    print(f"{len(new_weights)=}")

                    # Rescale the weights to sum to 1
                    norm_weights = new_weights/np.linalg.norm(new_weights, ord=1)

                    # loop through zip(sorted list of segments, row of new_weights that is sorted the same way) in bin
                    for new_weight, segment in zip(norm_weights, segments):
                        segment.weight = new_weight

                    # Make a nice df for looking at stuff
                    pd.set_option('display.colheader_justify', 'center')
                    df = pd.DataFrame({
                        'pcoords': pcoords[:,0],
                        'seg_id': seg_ids,
                        'weights': weights,
                    })

                    #if np.any(init_check):
                        #df['new_weights'] = new_weights
                        #df['norm_weights'] = norm_weights
                       
                      # df['cur_energy'] = d_ene
                       
                       # df['past_energy'] = dih_energies+vdw_energies+elec_energies
                        #df['temp_it'] = temp_it[(real_it)]
                        #df['temp_it+1'] =temp_it[(real_it+1)]
                    print("\n", df)


                # check if not initializing, then split and merge
                if np.any(init_check):
                    # These are the initial max and min weights
                    min_weight = min(new_weights)
                    max_weight = max(new_weights)

                    # track segid, weights
                    weight_array = np.array([seg_ids, new_weights]).T
                    
                    # For testing purposes
                    #weight_array = np.array((np.arange(10), (.01, .02, .03, .03, .04, .05, .06, .07, .08, .61))).T
                    
                    # track what is being split and how many times
                    # key is segid, value is num_splits
                    split_dict = {}
                  
                    # track merging segments
                    # list of lists of groups to merge
                    merge_list = []
                    
                    # Number of times through split merge loop
                    count = 1
                    debug = True

                    # While the spilt/merge condition is met


                      # While the spilt/merge condition is met
                    while max_weight > min_weight * 2:
                        if debug:
                            print("Number of times through the split/merge loop:", count)
                            count += 1

                            print(f"{weight_array=}")
                        
                        # Create an array of indices for the row of each maximum weight value
                        split_indices = np.asarray(
                            weight_array==np.max(weight_array[:,1])
                            ).nonzero()[:][0]
                        
                        # Gets the segid of the split
                        # Assumes the maxim(um/a) have the same segid
                        split_segid = int(weight_array[split_indices[0], 0])
                        if debug:
                            print(f"{split_indices=} {split_segid=}")
                        
                        # Get the values of the two lowest weights
                        merge_weights = weight_array[weight_array[:, 1].argsort()][:2, 1]
                        if debug:
                            print(f"{merge_weights=}")


                        # Get the indices for the merge
                        if merge_weights[0] == merge_weights[1]: # If the smallest weights are the same
                            # Get the indices of the list that correspond to the lowest weights
                            merge_indices = list(np.where(weight_array==merge_weights[0])[0])
                        else:
                            # Get the indices of the list that correspond to the lowest weights
                            merge_indices = [np.where(weight_array==x)[0] for x in merge_weights]
                            if debug:
                                print(f"{merge_indices=}")
                            if merge_indices[1].shape[0] != 1:  # If the next smallest weight has several indices
                                # Reset the second merge in the pair to be a random selection of the possible merge partners
                            
                                merge_indices[1] = merge_indices[1][
                                    random.randint(
                                    0, len(merge_indices[1]) - 1
                                        )
                                    ]
                            # Convert any arrays to ints
                            merge_indices = [int(x) for x in merge_indices]
                            if debug:
                                print(f"{merge_indices=}")


                                                
                        # Get the segids for the new merges
                        merge_segids = [int(weight_array[x, 0]) for x in merge_indices]
                        
                        # List of all segids currently being merged
                        current_merges = [y for x in merge_list for y in x]

                        # Test if we're violating the rules
                        # Cannot split a walker up for merging
                        if split_segid in current_merges or split_segid in merge_segids:
                            print("Tried to split something that is set to be merged!")
                            break
                        
                        # Cannot merge a walker up for splitting
                        if merge_segids[0] in split_dict or merge_segids[0] == split_segid or merge_segids[1] == split_segid or merge_segids[1] in split_dict:
                            print("Tried to merge something that is set to be split!")
                            break
                        
                        # if the split candidate is already being split
                        if split_segid in split_dict:
                            # Adjust the splitting to add in the new split
                            num_splits = split_dict[split_segid]
                            split_dict[split_segid] = num_splits + 1
                        else:
                            # Otherwise, add a new key for that segid
                            num_splits = 1
                            split_dict[split_segid] = 2
                        if debug:
                            print(f"{split_dict=}")
                        
                        # Update the weight_array to account for the split
                        new_split_weight = weight_array[split_indices[0], 1] * num_splits / (num_splits + 1)
                        for index in split_indices:
                            weight_array[index, 1] = new_split_weight

                        # Neither of the members of the merge have been merged before
                        missing = True
                        if debug:
                            print(f"{current_merges=}")
                        # Add in the merge
                        # If both segids are already being merged
                        if merge_segids[0] in current_merges and merge_segids[1] in current_merges:
                            if debug:
                                print("Both merging segids are already being merged")
                            # Find the two lists containing the segids
                            # Delete them from the list
                            for merge_group in merge_list:
                                if debug:
                                    print(f"{merge_group=}")
                                if merge_segids[0] in merge_group:
                                    first_list = list(merge_group)
                                    first_remove = merge_group 
                                    if debug:
                                        print(f"{merge_segids=} {merge_group=} {merge_list=}")
                                if merge_segids[1] in merge_group:
                                    second_list = list(merge_group)
                                    second_remove = merge_group
                                    if debug:
                                        print(f"{merge_segids=} {merge_group=} {merge_list=}")

                            merge_list.remove(first_remove)
                            merge_list.remove(second_remove)

                            # Add a merged list
                            merge_list.append([y for x in [first_list, second_list] for y in x])
                            missing = False
                       # If at most one of segids is already being merged
                            
                        else:
                            # Loop through the merges
                            for merge_group in merge_list:    
                                # if one part of the merge pair is already being merged, add the other to its group
                                if merge_segids[0] in merge_group:
                                    merge_group.append(merge_segids[1])
                                    missing = False
                                elif merge_segids[1] in merge_group:
                                    merge_group.append(merge_segids[0])
                                    missing = False
                        
                        # If neither merge member is already being merged, add a new merge
                        if missing:
                            merge_list.append(merge_segids)

                        if debug:
                            print(f"{merge_list=}")
                            walkers_added = 0
                            for key in split_dict:
                                walkers_added += split_dict[key] - 1
                            
                            walkers_removed = 0
                            for merge in merge_list:
                                walkers_removed += len(merge) - 1                       

                        # Update the weight_array to account for merging
                        # Replace one of the merged walkers with the new split
                        weight_array[merge_indices[0], :] = [split_segid, new_split_weight]
                        
                        # Update the weight of the other merged walker with the sum of the weights
                        weight_array[merge_indices[1], 1] = np.sum(merge_weights)

                        # Update the max/min weights
                        min_weight = min(weight_array[:, 1])
                        max_weight = max(weight_array[:, 1])
                    
                    # If there is split/merge
                    if split_dict or merge_list:
                        if debug:
                            walkers_added = 0
                            for key in split_dict:
                                walkers_added += split_dict[key] - 1
                            
                            walkers_removed = 0
                            for merge in merge_list:
                                walkers_removed += len(merge) - 1
                            print(f"{split_dict=} {merge_list=}")
                        
                        # Make a list for splitting segments
                        split_segments = []
                        
                        # Make a list for the number of splits corresponding to the above segments
                        split_into_per_segment = []
                        
                        # Loop through all the splits
                        for key in split_dict:
                            # Add in the segments and num splits for each split
                            split_segments.append(segments[seg_ids.index(key)])
                            split_into_per_segment.append(split_dict[key])

                        # Send to be split
                        self._split_by_data(bin, split_segments, split_into_per_segment)
                        
                        # Make a list containing lists of sengment objects to be merged together
                        to_merge = [[segments[seg_ids.index(id)] for id in group] for group in merge_list]
                        # Send for merging
                        self._merge_by_data(bin, to_merge)
                    else:
                        print("No split/merge this iteration")
        
        # another sanity check
        self._check_post()

        self.new_weights = self.new_weights or []

        log.debug('used initial states: {!r}'.format(self.used_initial_states))
        log.debug('available initial states: {!r}'.format(self.avail_initial_states))

























